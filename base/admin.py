from django.contrib import admin

from .models import Room, Topic, Message # Register your models here


# Register your models here.


# this is where you do crud operation in the admin for models

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
