from django.contrib.auth.models import AbstractUser,Permission, Group,BaseUserManager
from django.db import models



from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = []  # fields required when using createsuperuser command


  
