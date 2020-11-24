from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import StoriesSerializer
from .models import Story
from .decorators import forbid_fields

Writer = get_user_model()


class StoriesView(APIView):
    '''
        Clase exclusivo para control de stories.
        Todas las funciones a excepción de <get>,
        solo hacen lectura de una instancia de story
    '''
    serializer_class = StoriesSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        '''
            Json e.g.
                {
                    "story_id": <id>,
                    "writer" <id>
                }
        '''

        #queryset = Story.objects.filter(writer__email__exact=writer_email)
        writer_id = request.data.pop('writer')
        queryset = Story.objects.filter(writer=writer_id)
        serializer = StoriesSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
            Json e.g.

        '''
        writer = request.user
        data = request.data
        data['writer'] = writer.id

        serializer = StoriesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # TODO problema al serializar Writer, debe ser por la relacion FK, se puede guardar pero no retornar al response dentro y con formato JSON
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @forbid_fields
    def put(self, request):
        '''
            Se modifica con la siguiente estructura.
            {
                "id_story": "id_story",
                "modify":{
                    ...
                    "field_name": "new_value"
                }
            }
        '''
        try:
            id_story = request.data.get('id_story')
            modify = request.data.get('modify')
            story = Story.objects.get(id=id_story)
            for field, new_value in modify.items():
                old_value = getattr(story, field)  # get dinamico
                if old_value != new_value:
                    print("ENTROO")
                    setattr(story, field, new_value)  # set dinamico

            story.save()

            return Response({'Success': 'Updated'}, status=status.HTTP_200_OK)

        except:
            return Response({'Error': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        id_story = request.data.get('id_story')
        story = Story.objects.get(id=id_story)
        story.save()

        return Response({'Success': 'Deleted'}, status=status.HTTP_200_OK)


class StoriesListView(ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StoriesSerializer
