from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Thread(models.Model):
    """
    Thread model.
    Participants - must be only two users without existed thread between them.
    """
    participants = models.ManyToManyField(User, verbose_name="Participant", related_name='threads')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f'{self.id}'


class Message(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, related_name='messages')
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
