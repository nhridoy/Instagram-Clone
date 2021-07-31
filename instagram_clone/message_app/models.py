from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Messaging(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message_text = models.TextField(max_length=360, verbose_name='Write Message')
    message_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}\'s Message to {self.receiver}'
