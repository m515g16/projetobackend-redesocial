from rest_framework import serializers
from usuarios.serializers import UserPublicSerializer
from .models import Publication


class PublicationSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = ("id", "image", "text", "user", "public", "created_at")


class PublicationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ("id", "image", "text", "public", "created_at")
