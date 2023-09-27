from atexit import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser 

@admin.register(CustomUser)
class CustomUser(UserAdmin):
       add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email","password1", "password2"),
            },
        ),
    )