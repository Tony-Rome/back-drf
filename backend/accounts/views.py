import json
from django.contrib.auth import authenticate, get_user_model
from django.apps import apps
from django.db import models, connection
from django.forms.models import model_to_dict
from django.http import response
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import  ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from .models import Comment, Collaborator, Decision
from .serializers import WriterSerializer, CollaboratorSerializer, CommentSerializer, DecisionSerializer
from .decorators import custom_auth_writer, CustomAuth

Writer = get_user_model()


class SessionView(APIView):
    '''
        Clase vista solo para controlar login o logout.
        Valida tanto token, usuario, autenticación de request
        como tambien que token pertenezca a usuario que hace request.
    '''

    def post(self, request):  # LOGIN
        if request.user.is_anonymous:
            writer = authenticate(
                username=request.data.get('email'),
                password=request.data.get('password'))

            if writer is not None:
                token = Token.objects.create(user=writer)
                data = {
                    "email": writer.email,
                    "token": token.key or None
                }
                return Response(data=data, status=status.HTTP_200_OK)

        return Response({"error": "Access denied"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    @custom_auth_writer
    def put(self, request): # LOGOUT
        request.user.auth_token.delete()
        return Response(data={'success': 'logout'}, status=200)


class WriterView(APIView):

 #   authentication_classes = [SessionAuthentication, BasicAuthentication]
#    permission_classes = [IsAuthenticated]

    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):  # Obtener perfil
        email = request.user.email
        queryset = Writer.objects.get(email=email)
        serializer = WriterSerializer(queryset, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):  # Registrar

        data = request.POST.dict()  # QueryDict
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        writer = Writer.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)

        if writer:

            return Response({'success': f"{writer}"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'failed':'No se puede registrar'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    @permission_classes([IsAuthenticated])
    def put(self, request, *args, **kwargs):  # actualizar
        '''
            Se actualiza agregando campo "modify" con formato:

            {
                "email": "user_email",
                "modify":{
                    ...
                    "field_name": "new_value",
                    ...
                }
            }
        '''
        try:
            email = request.data.get('email')
            modify = request.data.get('modify')
            writer = Writer.objects.get(email=email)

            for key, value in modify.items():
                writer_value = getattr(writer, key)  # get dinamico
                if writer_value != value:
                    setattr(writer, key, value)  # set dinamico

            writer.save()

            return Response({'Success': 'Edited'}, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'Failed'}, status=status.HTTP_400_BAD_REQUEST)

    def change_email(self, email):
        pass
            #writer = Writer.objects.get(email=email)

            #writer_email = Writer.objects.filter(email=email).values_list('email', flat=True).first()

    @permission_classes([IsAuthenticated])
    def delete(self, request, *args, **kwargs):  #
        try:
            writer_email = request.data.get('email')
            writer = Writer.objects.get(email=writer_email)
            request.user.auth_token.delete()
            writer.delete()
            return Response({'Success': 'User deleted'}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response({'Error': 'Denied'}, status=status.HTTP_400_BAD_REQUEST)


class CollaboratorView(APIView):
    '''
        Clase para una persona si quiere o no ser colaborador,
        y administrar todas sus colaboraciones tanto story route como
        hopscotch
    '''

    def post(self, request):
        writer_id = request.user.id
        serializer = CollaboratorSerializer(data={'writer': writer_id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Succss': 'Enabled collaborator'}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        collaborator_id = request.data.get('collaborator_id')
        writer_id = request.user.id
        collaborator = Collaborator.objects.filter(id=collaborator_id, writer=writer_id)
        collaborator.delete()
        return Response({'Success': 'Deleted collaborator'}, status=status.HTTP_200_OK)


class CollaboratorListView(ListAPIView):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer


class CommentView(APIView):

    # tables = connection.introspection.table_names()  Obtiene nombres de todas las tablas
    serializer_class = CommentSerializer

    def get(self, request):
        writer = request.user
        queryset = Comment.objects.filter(writer=writer)
        serializer = CommentSerializer(queryset, many=True)


        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
            Json e.g.
                {   
                "writer": 8,
                "type_id": 1,
                "type_post": "story",
                "content": "Primer comentario para story"
            }
        '''
        writer_id = request.data.pop('writer')
        writer = Writer.objects.get(id=writer_id)
        data = request.data
        data['writer'] = writer
        comment = Comment.objects.create(**data)
        comment_dict = model_to_dict(comment)
        return Response({'Success': comment_dict}, status=status.HTTP_201_CREATED)

    def put(self, request):
        '''
                    Json e.g.
                        {
                        "writer": 8,
                        "comment_id": 2,
                        "content": "Primer comentario para story"
                    }
         '''
        writer_id = request.data.pop('writer')
        writer = Writer.objects.get(id=writer_id)
        comment_id = request.data.pop('comment_id')
        content = request.data
        comment = Comment.objects.filter(id=comment_id, writer=writer).first()
        serializer = CommentSerializer(comment, content)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('OK')

    def delete(self, request):
        comment_id = request.data.pop('comment_id')
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return Response({'Success': 'Deleted'}, status=status.HTTP_200_OK)


class CommentListView(ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class DecisionView(APIView):

    def get(self, request):
        writer = request.user
        queryset = Decision.objects.filter(writer=writer)
        serializer = DecisionSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
            JSON e.g.
            {   
            "writer": 8,
            "state": 0,
            "type_id": 1,
            "type_post": "story"
            }
        '''
        data = request.data
        serializer = DecisionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'Success': serializer.data}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        writer = request.user
        decision_id = request.data.get('decision_id')
        decision = Decision.objects.get(id=decision_id, writer=writer)
        decision.delete()

        return Response({'Success': 'Deleted'}, status=status.HTTP_202_ACCEPTED)


class WriterList(ListCreateAPIView):

    queryset = Writer.objects.all()
    serializer_class = WriterSerializer
