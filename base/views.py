from django.http import HttpResponse
from django.shortcuts import render, redirect
from base.helpers import Helper
import logging
from .models import Room, Topic, User
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
helper = Helper
logger = logging.getLogger(__name__)
info_logger = logging.getLogger('info_logger')


def loginPage(request):  # python has a default login function, so never use login as a function name

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
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

    context = {}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

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

    topics = Topic.objects.all()

    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}

    return render(request, 'base/home.html', context)


def rooms(request):  # pass room id as a parameter
    return render(request, 'base/room.html')


def roomDetails(request, room_id, room_name):  # pass room id as a parameter

    # This is how you fetch data by id

    room = Room.objects.get(id=room_id)

    logger.warning(f"room id {room_id}")

    if room is None:

        return HttpResponse('404: Room not found')

    else:

        return render(request, 'base/room_detail.html', {'room': room})


@login_required(login_url='login')
def createRoom(request):
    context = {'form': RoomForm()}

    if request.method == 'POST':
        # request.POST.get('name') gets the individual data
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, room_id):
    room = Room.objects.get(id=room_id)

    form = RoomForm(instance=room)  # meaning, the form will be refilled with the instance of room values. The form
    # values should match the fields though, else it won't work

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)  # This will update the instance
        if form.is_valid():
            if form.is_valid():
                form.save()
                return redirect('home')

    context = {'form': form}

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
