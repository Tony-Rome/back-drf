from rest_framework import serializers
from .models import StoryRoute, OrderByRoute
from accounts.models import Collaborator
from stories.serializers import StoriesSerializer
from stories.models import Story


class StoriesRoutesSerializer(serializers.ModelSerializer):
    '''
        JSON EXAMPLE:
            {
            "writer": 8,
            "id_story_route": 100,
            "collaborators": [1,2, 3],
            "stories": [4, 5 ,6]
            }
    '''
    stories = serializers.ListField(allow_null=True, allow_empty=True)
    collaborators = serializers.ListField(allow_null=True, allow_empty=True, )

    class Meta:
        model = StoryRoute
        fields = ('id', 'writer', 'collaborator', 'stories', 'collaborators',)

    def update(self, instance, validated_data):
        print("VALId DATA: ", validated_data)
        print("INSTANCE: ", instance)
        if validated_data.get('stories'):
            print("ENTRO A SOTRIES")
            stories = validated_data.pop('stories')
            print("STORIES: ",stories )
            for id_story in stories:
                story = Story.objects.get(id=id_story)
                instance.story_set.add(story)
        if validated_data.get('collaborators'):
            print("ENTRO A COLL")
            collaborators = validated_data.pop('collaborators')
            print("COLLA: ", collaborators)
            for id_collaborator in collaborators:
                collaborator = Collaborator.objects.get(id=id_collaborator)
                instance.collaborator = collaborator
        #stories_list = validated_data.get('stories')
        #print("LIST: ", stories_list)
        #for story in stories_list:
        #    st = Story.objects.get(id=story)
        #    instance.story_set.add(st)
        instance.save()
        print("ALL STORIES: ", instance.story_set.all())
        print("ALL COLL: ", instance.collaborator)
        return instance


class OrderByRouteSerializer(serializers.ModelSerializer):
    '''
        Json example:
            {
            "writer": 8,
            "collaborator": 2,
            "id_story_route": 100,
            "order_route":[
                {"id_story": 1, "position": 2},
                {"id_story": 2, "position": 3},
                {"id_story": 4, "position": 1},
                {"id_story": 7, "position": 5},
                {"id_story": 8, "position": 4}
            ]
        }
    '''

    order_route = serializers.ListField(allow_null=True, allow_empty=True)
    writer = serializers.IntegerField()
    collaborator = serializers.IntegerField()
    id_story_route = serializers.IntegerField()

    class Meta:
        model = OrderByRoute
        fields = ['order_route', 'writer', 'collaborator', 'id_story_route']

    def create(self, validated_data):
        id_story_route = validated_data.pop('id_story_route')
        story_route = StoryRoute.objects.get(id=id_story_route)

        order_route_list = validated_data.pop('order_route')
        order_route_list.sort(key=lambda element: element['position'], reverse=True)

        story_info = order_route_list[-1]
        del(order_route_list[-1])

        order_route = OrderByRoute.objects.create(story_route=story_route, story_id=story_info['id_story'])
        order_route.story_child = self.story_child(order_route_list=order_route_list, position=len(order_route_list))
        order_route.save()

        return order_route

    def story_child(self, order_route_list, position):

        if len(order_route_list) == 1:
            story_info = order_route_list[0]
            order_route = OrderByRoute.objects.create(story_id=story_info['id_story'])
            return order_route

        story_info = order_route_list[position-1]

        del order_route_list[position-1]
        order_route = OrderByRoute.objects.create(
            story_id=story_info['id_story'],
            story_child=self.story_child(
                order_route_list=order_route_list,
                position=position-1
            )
        )

        return order_route
       # order_route.story_route =
       # order_route.story_id =
       # order_route.story_child =




