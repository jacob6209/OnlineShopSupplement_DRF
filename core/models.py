from django.contrib.auth.models import AbstractUser,Permission, Group
from django.db import models


class CustomUser(AbstractUser):
    # phone_number = models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = []

  
