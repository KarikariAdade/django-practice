from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User


# This is where you create your model form, you have to import your models that you want to create the forms for

class RoomForm(ModelForm):
    # Set the metadata of the forms
    class Meta:
        model = Room
        # fields = '__all__'  # this value will create the form based on the room model table columns that we have
        fields = '__all__'  # this value will create the form based on the room model table columns that we have
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
