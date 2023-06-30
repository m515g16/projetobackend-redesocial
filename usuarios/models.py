from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    class Meta:
        ordering = ["name"]

    email = models.CharField(max_length=127, unique=True)
    name = models.CharField(max_length=127)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
