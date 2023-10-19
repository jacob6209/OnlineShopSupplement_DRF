from pickle import NONE
from django.contrib.auth.models import AbstractUser,Permission, Group,BaseUserManager
from django.db import models



from django.contrib.auth.models import AbstractUser



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # username=NONE
    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = []  # fields required when using createsuperuser command

    objects = CustomUserManager()

    def __str__(self):
     return self.email
