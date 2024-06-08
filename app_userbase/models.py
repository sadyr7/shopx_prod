from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import CustomUserManager
from .validators import validate_password_strength
from django.core.validators import RegexValidator

class BaseUser(models.Model):
    email_or_phone = models.CharField(max_length= 30,unique = True,null= True, blank=True)
    email = models.EmailField("Email",unique=True,max_length=255,null=True,blank=True)
    phone_number = models.CharField(
        max_length=13,
        validators=[RegexValidator(r"^\+996\d{9}$")],
        blank=True,
        null=True,
    )
    
    auth_token_refresh = models.CharField(max_length=255, null=True, blank=True)
    auth_token_access = models.CharField(max_length=255, null=True, blank=True)
    
    username = models.CharField(max_length= 30, verbose_name="Имя",null=True, blank=True)
    surname = models.CharField(max_length= 30, verbose_name="Фамилия",null=True, blank=True)
    password = models.CharField("password",validators=[validate_password_strength], max_length=128)
    code = models.CharField(max_length=6, blank=True)
    created_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='usual/profiles/', blank=True, null=True)
    # number = models.CharField(max_length= 30,unique=True,null= True, blank=True)
    device_token = models.CharField(max_length = 100, verbose_name = 'токен от ios/android')

    objects = CustomUserManager()


    def __str__(self) -> str:
        return f"{self.email_or_phone}"
    
    class Meta:
        abstract = True

    USERNAME_FIELD = 'email_or_phone'
    REQUIRED_FIELDS = ['username']


