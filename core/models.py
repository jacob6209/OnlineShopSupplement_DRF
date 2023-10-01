from django.contrib.auth.models import AbstractUser,Permission, Group
from django.db import models


class CustomUser(AbstractUser):
    # phone_number = models.CharField(max_length=255)
    email=models.EmailField(unique=True)
       # Your custom fields and methods...

  
