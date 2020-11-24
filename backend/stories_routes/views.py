from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import StoryRoute, OrderByRoute
from .serializars import StoriesRoutesSerializer, OrderByRouteSerializer
from .decorators import has_story_route
from accounts.models import Collaborator, Writer
from rest_framework import serializers
from django.forms.models import model_to_dict
class StoriesRoutesView(APIView):

    '''
        Clase exclusica para administar las rutas de historia

        Para def post() el JSON debe ser formato:
        {
            "collaborators": [  --> Parametro opcional
                number, number, number, number ...
            ]
        }
    '''

    permission_classes = [IsAuthenticated]
    #serializer_class = StoriesRoutesSerializer

    def get(self, request):
        writer_email = request.user.email
        queryset = StoryRoute.objects.filter(writer__email__exact=writer_email)
        serializer = StoriesRoutesSerializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        id_writer = request.data.get('writer')
        writer = Writer.objects.get(id=id_writer)
        story_route = StoryRoute.objects.create(writer=writer)
        story_route_json_dict = model_to_dict(story_route)
        return Response({'CREATED': story_route_json_dict}, status=status.HTTP_200_OK)

    def put(self, request):
        print("REQUEST: ", request.data)
        id_story_route = request.data.get('id_story_route')
        story_route = StoryRoute.objects.get(id=id_story_route)
        serializer = StoriesRoutesSerializer(story_route, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Success': 'Story route updated'}, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            id_story_route = request.data.get('id')
            story_route = StoryRoute.objects.get(id=id_story_route)
            story_route.delete()
            return Response({'Success': 'Story route delete'})
        except:
            return Response({'Error': 'Bad request'}, status=status.HTTP_200_OK)


class StoriesRoutesListView(ListAPIView):
    queryset = StoryRoute.objects.all()
    serializer_class = StoriesRoutesSerializer


class OrderByRouteView(APIView):
    '''
        {
        "writer": 8,
        "id_story_route": 100,
        "collaborators": [1,2, 3],
        "stories": [4, 5 ,6]
        }
    '''

    permission_classes = [IsAuthenticated]
    serializer_class = OrderByRouteSerializer

    def get(self, request):
        writer_email = request.user.email
        queryset = OrderByRoute.objects.filter(writer__email__exact=writer_email)
        serializer = OrderByRouteSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        #id_writer = request.data.pop('id_writer')
        #writer = Writer.objects.get(id=id_writer)
        #serializer = OrderByRouteSerializer(data=)
        #writer = request.user
        data = request.data
        serializer = OrderByRouteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Success': 'Created'}, status=status.HTTP_201_CREATED)


'''
        data = request.data
        data['writer'] = request.user.id
        serializer = StoriesRoutesSerializer(data=data, context={'collaborators': data['collaborators']})
        serializer.is_valid()
        serializer.save()


        return Response({'Success':'Created'}, status=status.HTTP_201_CREATED)
        '''