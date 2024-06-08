from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email_or_phone=None,password=None, **extra_fields):


        user = self.model(email_or_phone=email_or_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_or_phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email_or_phone=email_or_phone, password=password, **extra_fields)
