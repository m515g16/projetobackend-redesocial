from rest_framework import serializers
from usuarios.serializers import UserPublicSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    publication_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "created_at", "user", "publication_id")
