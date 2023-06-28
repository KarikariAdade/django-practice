from django.urls import path
from . import views

urlpatterns = [
    # Path takes 3 params, url, and the view you're returning (like controller and its function) and the route/path name
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('room/', views.rooms, name="room"),
    path('room/details/<int:room_id>/<str:room_name>/', views.roomDetails, name="room.details"),
    path('create-room', views.createRoom, name="room.create"),
    path('update-room/<int:room_id>', views.updateRoom, name="room.update"),
    path('update-delete/<int:room_id>', views.deleteRoom, name="room.delete"),
    path('message-delete/<int:message_id>', views.deleteMessage, name="message.delete"),
    path('profile/<int:user_id>', views.userProfile, name="user.profile"),
    path('profile/update/', views.updateUser, name="user.update"),
    path('topics/', views.topicsPage, name="topics"),
    path('activities/', views.activityPage, name="activities")
]