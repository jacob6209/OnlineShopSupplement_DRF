from django.contrib.auth.models import AbstractUser,Permission, Group
from django.db import models


class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
       # Your custom fields and methods...

  
