from django.http import HttpResponse
from django.shortcuts import render, redirect
from base.helpers import Helper
import logging
from .models import Room, Topic, User, Message
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
helper = Helper
logger = logging.getLogger(__name__)
info_logger = logging.getLogger('info_logger')


def loginPage(request):  # python has a default login function, so never use login as a function name

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user is None:
                messages.error(request, 'User does not exist')
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Username or password incorrect')
        except:
            messages.error(request, 'User does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()  # imported from django library
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # commit = false, enables us to get the user object
            user.username = user.username.lower()
            user.save()
            login(request, user)  # Log user in
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})


@login_required(login_url='login')
def home(request):
    # This is how you pass values to pages

    # queryset = ModelName.objects.all()/filer()/get()/exclude();

    q = request.GET.get('q') if request.GET.get('q') is not None else ''  # Get the url parameter q if it exists

    # rooms = Room.objects.filter(topic__name__icontains=q)  # icontains is another version of 'LIKE'
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |  # search by relationship (room->topic->name->like->q
        Q(name__icontains=q) |  # room name like q
        Q(description__icontains=q)
    )  # icontains is another version of 'LIKE', Q is a query utility imported

    topics = Topic.objects.all()[0:5]

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))  # View activities per topic
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}

    return render(request, 'base/home.html', context)


def rooms(request):  # pass room id as a parameter
    return render(request, 'base/room.html')


def roomDetails(request, room_id, room_name):  # pass room id as a parameter

    # This is how you fetch data by id

    room = Room.objects.get(id=room_id)

    room_messages = room.message_set.all().order_by('-created')  # This gets all the relationship messages (hasMany
    # in laravel). room_relationship_name_set.all()

    participants = room.participants.all()

    # logger.warning(f"room id {room_id}")

    if request.method == 'POST':
        message = Message.objects.create(  # this is how you manually add data to a db
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)  # Adds user to participants table
        return redirect('room.details', room_id=room_id, room_name=room.name)

    if room is None:
        return HttpResponse('404: Room not found')
    else:
        return render(request, 'base/room_detail.html',
                      {'room': room, 'room_messages': room_messages, 'participants': participants})


@login_required(login_url='login')
def createRoom(request):
    topic = Topic.objects.all()
    context = {'form': RoomForm(), 'topics': topic}

    if request.method == 'POST':
        # request.POST.get('name') gets the individual data

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, room_id):
    room = Room.objects.get(id=room_id)
    topic = Topic.objects.all()

    form = RoomForm(instance=room)  # meaning, the form will be refilled with the instance of room values. The form
    # values should match the fields though, else it won't work

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        # form = RoomForm(request.POST, instance=room)  # This will update the instance
        # if form.is_valid():
        #     if form.is_valid():
        #         form.save()
        #         return redirect('home')

    context = {'form': form, 'room': room, 'topics': topic}

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, room_id):
    room = Room.objects.get(id=room_id)
    context = {'room': room, 'form': RoomForm()}

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        if room.id != '':
            room.delete()
            return redirect('home')

    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, message_id):
    message = Message.objects.get(id=message_id)
    if request.user.id == message.user.id:
        message.delete()
        return redirect('room.details', room_id=message.room_id, room_name=message.room.name)
    else:
        messages.error(request, 'You do not have the permission to delete this message')

    return redirect('room.details', room_id=message.room_id, room_name=message.room.name)


@login_required(login_url='login')
def userProfile(request, user_id):
    user = User.objects.get(id=user_id)
    if user is None:
        messages.error(request, 'User does not exist')

    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)  # Get initial user value

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user.profile', user_id=user.id)
    return render(request, 'base/update_user.html', {'form': form, 'user': user})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''  # Get the url parameter q if it exists
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {"room_messages": room_messages})