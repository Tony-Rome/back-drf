from rest_framework import serializers
from .models import Story
from accounts.models import Decision


class StoriesSerializer(serializers.ModelSerializer):

    state_false = serializers.SerializerMethodField(required=False ,read_only=True)
    state_true = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Story
        fields = '__all__'

    def get_state_false(self, obj):
        state_false = Decision.objects.filter(type_id=obj.id, type_post="story", state=False).count()
        return state_false

    def get_state_true(self,obj):
        state_true = Decision.objects.filter(type_id=obj.id, type_post="story", state=True).count()
        print("COUNT: ",state_true)
        return state_true
