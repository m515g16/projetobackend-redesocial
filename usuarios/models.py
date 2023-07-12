from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        ordering = ["name"]

    email = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=60)
    birthdate = models.DateField(null=True)
    perfil = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    followers = models.ManyToManyField(
        "usuarios.User", through="usuarios.Followers", related_name="seguidores"
    )

    friend_solicitations = models.ManyToManyField(
        'self', symmetrical=False, through="usuarios.FriendSolicitations", related_name="solicitacao_amizade"
    )


class Followers(models.Model):
    user = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="followed_user"
    )

    follower = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="follower_user"
    )


class FriendSolicitations(models.Model):
    user = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="friend_solicited"
    )

    friend = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="friend_request"
    )

    pendding = models.BooleanField(default=True)
    accepted = models.BooleanField(default=False)
