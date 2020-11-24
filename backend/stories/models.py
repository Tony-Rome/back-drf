from django.db import models


class Story(models.Model):

    writer = models.ForeignKey("accounts.writer", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=511)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    #  TODO agregar campo para cargar imagen
    story_route = models.ForeignKey("stories_routes.storyroute", on_delete=models.CASCADE, null=True, blank=True)
    hopscotch = models.ForeignKey("hopscotch.hopscotch", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'story'

    def __str__(self):
        return f"{self.id} {self.writer.email} - {self.id} {self.title}"


class Hashtag(models.Model):

    story = models.ForeignKey("story", on_delete=models.CASCADE)
    hashtag = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hashtag'
        
