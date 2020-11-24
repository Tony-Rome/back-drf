from rest_framework import serializers
from .models import Hopscotch
from accounts.serializers import CollaboratorSerializer
from stories.serializers import StoriesSerializer
from accounts.models import Collaborator
from django.db import transaction
'''
class CollaboratorSerializer(serializers.ModelSerializer):

    #hopscotchs = HopscotchSerializer(many=True)
    #stories_routes = StoriesRoutesSerializer(many=True)

    class Meta:
        model = Collaborator
        fields = ['writer', 'range', 'timestamp']  # Puede que de error timestamp

    #def create(self, validate_data):
'''

class HopscotchSerializer(serializers.ModelSerializer):
    '''
        JSON:
            {   
                "writer": 8,
                "collaborators":
                    [
                        { "writer": 8},
                        {"writer": 3},
                        {"writer": 5}
                    ]
            }
    '''

    collaborators = CollaboratorSerializer(many=True)


    class Meta:
        model = Hopscotch
        fields = ['collaborators', 'writer']  # Campos obligatrios para el json

    def create(self, validate_data):
        print("VALIDATE DATA: ", validate_data)
        collaborators = validate_data.pop('collaborators')
        hopscotch = Hopscotch.objects.create(**validate_data)

        for collaborator in collaborators:
            c = Collaborator.objects.get(writer_id=collaborator['writer'].id)
            hopscotch.collaborator = c
            hopscotch.save()
            print("RESULT: ", c.hopscotch_set.all())


        print(hopscotch)
        return Hopscotch
