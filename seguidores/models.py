from django.db import models

class Seguidor(models.Model):
    seguidor = models.BooleanField(null=True, default=False)
    amigo = models.BooleanField(null=True, default=False)
