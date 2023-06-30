from django.db import models

class Curtida(models.Model):
    curtido = models.BooleanField(null=True, default=False)
    
