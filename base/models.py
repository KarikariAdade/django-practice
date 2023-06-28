from django.db import models
from django.contrib.auth.models import User  # Import user model


# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)  # null is for column being null, blank is for form field
    # being null
    participants = models.ManyToManyField(User, related_name='participants',
                                          blank=True)  # many to many fields, blank=True means i can submit a form without necessarily adding participants
    updated = models.DateTimeField(auto_now=True)  # auto_now=True, means it'll automatically take a timestamp
    created = models.DateTimeField(auto_now_add=True)  # auto_now_add=True, means it'll take a timestamp of the first

    # time the thing was created

    class Meta:
        ordering = ['-updated', '-created']  # This fetched the rooms and order by updated first, before created

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Set up user relationship for the messages. So messages
    # would belong to users. This is a one to many relationship
    # this is a one-to-many relationship. meaning room can have multiple messages
    # SET_NULL means message will not be deleted if room is deleted, cascade is the opposite
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]  # Gets the first 50 characters
