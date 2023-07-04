from django.db import models
from django.contrib.auth.models import AbstractUser

class FriendSituation(models.TextChoices):
    pendding = "Pendente"
    accepted = "Aceito"
    denied = "Negado"

class User(AbstractUser):
    class Meta:
        ordering = ["name"]

    email = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=60)
    birthdate = models.DateField(null=True)
    perfil = models.CharField(max_length=180, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    
    followers = models.ManyToManyField(
        "usuarios.User", through="usuarios.Follower", related_name="seguidores"
    )

    friend_solicitations = models.ManyToManyField(
        "usuarios.User", through="usuarios.Friend", related_name="solicitacao_amizade"
    )

    # @property
    # def friends(self):
    #     return User.objects.filter(friend__friend=self, friend__accepted=True)
    
    @property
    def friends(self):
        return User.objects.filter(friend__friend=self, friend__situation="Aceito")

class Follower(models.Model):
    user = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="followed_user"
    )

    follower = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="follower_user"
    )

class Friend(models.Model):
    user = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="user"
    )

    friend = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="friend"
    )

    # pendding = models.BooleanField(default=True)
    # accepted = models.BooleanField(default=False)
    # solicited = models.BooleanField(default=True) 

    situation = models.CharField(max_length=20, choices=FriendSituation.choices, default=FriendSituation.pendding)
