from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])  # Request that you want, can accept [] of methods ['GET', 'POST']
def getRoute(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)  # Many being set to true, means we're serializing a lot of objects,
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, room_id):
    rooms = Room.objects.get(id=room_id)
    serializer = RoomSerializer(rooms, many=False)  # Many being set to False, means we're serializing just one object,
    return Response(serializer.data)
