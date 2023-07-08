from rest_framework import serializers
from usuarios.serializers import UserPublicSerializer
from publicacoes.models import Publication
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    publication_id = serializers.IntegerField(write_only=True)

    def validate_publication_id(self, value):
        if not Publication.objects.filter(pk=value).exists():
            raise serializers.ValidationError(detail="Not found")

        return value

    class Meta:
        model = Like
        fields = ("id", "user", "publication_id")


class PublicationLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ("id", "image", "text", "created_at")


class LikeUserSerializer(serializers.ModelSerializer):
    publication = PublicationLikeSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ("id", "publication")
