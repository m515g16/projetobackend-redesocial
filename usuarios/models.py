from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        ordering = ["name"]

    email = models.CharField(max_length=127, unique=True)
    name = models.CharField(max_length=127)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    follower_friend = models.ManyToManyField(
        "usuarios.User", through="usuarios.FollowerFriends", related_name="seguidores"
    )

class FollowerFriends(models.Model):
    usuario = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="followed_user"
    )

    seguidor = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="follower_user"
    )

    amigo = models.BooleanField(null=True, default=False)
    
    
