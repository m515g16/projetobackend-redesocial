from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    email = models.CharField(max_length=127, unique=True)
    birthdate = models.DateField()
    

