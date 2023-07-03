from django.db import models


class Publication(models.Model):
    image = models.CharField(max_length=180, null=True)
    text = models.CharField(max_length=2500)
    public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="user_publication"
    )
