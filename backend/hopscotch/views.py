from django.shortcuts import render
from .models import Hopscotch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HopscotchSerializer


class HopscotchView(APIView):

    serializer_class = HopscotchSerializer

    def get(self, request):
        writer_id = request.user.id
        queryset = Hopscotch.objects.filter(writer=writer_id)
        serializer_class = HopscotchSerializer(queryset, many=True)

        return Response(data=serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        collaborators = request.data
        print(type(collaborators))
        #collaborators['writer'] = request.user.id
        #print("COLLAB: ", collaborators)

        serializer = HopscotchSerializer(data=collaborators)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

