from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email_or_phone=None,password=None, **extra_fields):


        user = self.model(email_or_phone=email_or_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
