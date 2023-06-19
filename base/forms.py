from django.forms import ModelForm
from .models import Room


# This is where you create your model form, you have to import your models that you want to create the forms for

class RoomForm(ModelForm):
    # Set the metadata of the forms
    class Meta:
        model = Room
        # fields = '__all__'  # this value will create the form based on the room model table columns that we have
        fields = '__all__'  # this value will create the form based on the room model table columns that we have
