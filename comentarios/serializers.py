from rest_framework import serializers
from usuarios.serializers import UserPublicSerializer
from publicacoes.models import Publication
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    publication_id = serializers.IntegerField()

    def validate_publication_id(self, value):
        if not Publication.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Not found publication")

        return value

    class Meta:
        model = Comment
        fields = ("id", "text", "created_at", "user", "publication_id")


class CommentUserSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "created_at", "user")
