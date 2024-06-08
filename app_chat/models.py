from django.db import models
from app_user.models import User





class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    user1 = models.ForeignKey(User, related_name='rooms_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='rooms_user2', on_delete=models.CASCADE)
    is_deleted_user1 = models.BooleanField(default=False)
    is_deleted_user2 = models.BooleanField(default=False)

    def is_fully_deleted(self):
        return self.is_deleted_user1 and self.is_deleted_user2


    def __str__(self) -> str:
        return f"{self.name}"

    # class Meta:
    #     ordering = ['-created_at']




class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.id}'
    class Meta:
        ordering = ('date_added',)



