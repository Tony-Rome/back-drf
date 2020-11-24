from django.db import models


class Hopscotch(models.Model):

    writer = models.ForeignKey("accounts.writer", on_delete=models.CASCADE)
    collaborator = models.ForeignKey("accounts.collaborator", on_delete=models.CASCADE, null=True, blank=True)
    state = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'hopscotch'

    def __str__(self):
        return f"Hopscotch {self.id}"
