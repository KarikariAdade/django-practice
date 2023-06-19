from django.urls import path
from . import views

urlpatterns = [
    # Path takes 3 params, url, and the view you're returning (like controller and its function) and the route/path name
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name="home"),
    path('room/', views.rooms, name="room"),
    path('room/details/<int:room_id>/<str:room_name>/', views.roomDetails, name="room.details"),
    path('create-room', views.createRoom, name="room.create"),
    path('update-room/<int:room_id>', views.updateRoom, name="room.update"),
    path('update-delete/<int:room_id>', views.deleteRoom, name="room.delete")
]