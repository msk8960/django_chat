from django.db import models
from django.contrib import auth

class User(models.Model):
    user = models.OneToOneField(auth.models.User, on_delete=models.CASCADE)
    is_online = models.BooleanField()

    def __str__(self):
        return self.user.username

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
