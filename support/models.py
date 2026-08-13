from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    question = models.TextField()

    answer = models.TextField(
        blank=True,
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:30]