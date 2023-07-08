from django.db import models

class Comment(models.Model):
    text = models.CharField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="user_commet"
    ) 

    publication = models.ForeignKey(
        "publicacoes.Publication", on_delete=models.CASCADE, related_name="comment_publication"
    ) 