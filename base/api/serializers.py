from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer):
    # just like form classes, this takes a minimum of two fields, the model and the fields you want to supply to the api
    class Meta:
        model = Room
        fields = '__all__'
