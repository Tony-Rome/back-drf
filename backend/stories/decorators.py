from rest_framework.response import Response
from rest_framework import status


def forbid_fields(function):

    def decorator(obj, request):

        prohibited_fields = ['id', 'writer', 'hopscotch', 'story_route', 'timestamp']
        fields = request.data.get('modify')

        for key, value in fields.items():
            if key in prohibited_fields:
                return Response({'Error': 'Denied'}, status=status.HTTP_401_UNAUTHORIZED)

        return function(self=obj, request=request)

    return decorator
