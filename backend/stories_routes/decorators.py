from rest_framework.response import Response
from rest_framework import status
from .models import StoryRoute, OrderByRoute


def has_story_route(function):

    def decorator(obj, request):
        data = request.data
        if len(data) != 1:
            return Response({'Error': 'No puede ser creado'}, status=status.HTTP_400_BAD_REQUEST)
        return function(self=obj, request=request)

    return decorator

