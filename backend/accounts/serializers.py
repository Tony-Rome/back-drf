from abc import ABC
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from .models import Comment, Decision, Collaborator
Writer = get_user_model()


class WriterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Writer
        fields = ['email', 'first_name', 'last_name', 'signing', 'web_site']
        #exclude = ['password', 'last_login']


 #   def create(self, validated_data):
#        pass


class CollaboratorSerializer(serializers.ModelSerializer):

    #hopscotchs = HopscotchSerializer(many=True)
    #stories_routes = StoriesRoutesSerializer(many=True)

    class Meta:
        model = Collaborator
        fields = ['writer', 'range', 'timestamp']  # Puede que de error timestamp

    #def create(self, validate_data):


class CommentSerializer(serializers.ModelSerializer):

    writer = serializers.CharField(required=False)

    class Meta:
        model = Comment
        fields = ['id', 'writer', 'type_post', 'type_id', 'content']

    def update(self, instance, validated_data):
        content = validated_data['content']
        instance.content = content
        instance.save()
        return instance


class DecisionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Decision
        fields = ['writer', 'state', 'type_post', 'type_id']

#    def create(self, validated_data):
#        print("VALID: ", validated_data)
#        return Decision
