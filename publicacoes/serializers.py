from rest_framework import serializers
from usuarios.serializers import UserSerializer
from .models import Publication


class PublicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = ("id", "image", "text", "user", "public", "created_at")
