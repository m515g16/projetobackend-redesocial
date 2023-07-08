from django.db import models

class Like(models.Model):
    user = models.ForeignKey(
        "usuarios.User", on_delete=models.CASCADE, related_name="user_like"
    ) 

    publication = models.ForeignKey(
        "publicacoes.Publication", on_delete=models.CASCADE, related_name="publication_like"
    )  
    
    
