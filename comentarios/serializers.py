from rest_framework import serializers
from usuarios.serializers import UserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    publication_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ("id", "text", "created_at", "user", "publication_id")
