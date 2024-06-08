from django.db import models
from app_user.models import User


class SupportServiceRoom(models.Model):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE,related_name='admin_rooms')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_rooms')
    slug = models.SlugField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"




class SupportServiceMessage(models.Model):
    support_room = models.ForeignKey(SupportServiceRoom, related_name='support_messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='support_messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.id}'
    class Meta:
        ordering = ('date_added',)