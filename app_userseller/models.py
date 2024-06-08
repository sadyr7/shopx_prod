from django.db import models
from app_userbase.models import BaseUser
from app_user.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import CustomUserManager



class SellerProfile(BaseUser,AbstractBaseUser, PermissionsMixin):

    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile',blank=True,null=True)
    is_seller = models.BooleanField(default=False)
    
    shop_name = models.CharField(max_length=255)
    instagram_link = models.URLField(null=True, blank=True)
    whatsapp_link = models.URLField(blank=True, null=True)
    tiktok_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)


    
    def __str__(self) -> str:
        return f'{self.email_or_phone}'
    
    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = verbose_name

    objects = CustomUserManager()

class CategorySC(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title}"

SellerProfile._meta.get_field('groups').remote_field.related_name = 'seller_groups'
SellerProfile._meta.get_field('user_permissions').remote_field.related_name = 'seller_permissions_set'