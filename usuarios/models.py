from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    email = models.CharField(max_length=127, unique=True)
    full_name = models.CharField(max_length=127)
    birthdate = models.DateField()
    

