from django.db import models


class StoryRoute(models.Model):

    writer = models.ForeignKey("accounts.writer", on_delete=models.CASCADE)
    collaborator = models.ForeignKey("accounts.collaborator", on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'storyroute'

    def __str__(self):
        return f"Story route: {self.id}"


class OrderByRoute(models.Model):

    story_route = models.ForeignKey("storyroute", on_delete=models.CASCADE, null=True, blank=True)
    story_child = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    story_id = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'order_route'

    def __str__(self):
        return f"Order route: {self.id}"


