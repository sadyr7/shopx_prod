from app_userbase.models import BaseUser
from django.db import models
from .usermanager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin



class User(BaseUser,AbstractBaseUser, PermissionsMixin):
    
    address = models.CharField(max_length=255,null=True,blank=True)
    is_usual = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.username}"
    
    objects = CustomUserManager()


    
    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = verbose_name

    USERNAME_FIELD = 'email_or_phone'
    REQUIRED_FIELDS = ['username']

User._meta.get_field('groups').remote_field.related_name = 'user_groups'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_permissions_set'


