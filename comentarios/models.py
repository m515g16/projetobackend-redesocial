from django.db import models

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="user_commet"
    ) 

    publication = models.ForeignKey(
        "publicacoes.Publication", on_delete=models.CASCADE, related_name="comment_publication"
    ) 