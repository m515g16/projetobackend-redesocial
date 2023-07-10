from rest_framework import serializers
from usuarios.serializers import UserPublicSerializer
from curtidas.models import Like
from curtidas.serializers import LikeSerializer
from comentarios.models import Comment
from comentarios.serializers import CommentSerializer
from .models import Publication


class PublicationSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = ("id", "image", "text", "user", "public", "created_at")


class PublicationUserSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_likes(self, obj):
        likes_publication = Like.objects.filter(publication=obj)
        serializer = LikeSerializer(likes_publication, many=True)

        return serializer.data

    def get_comments(self, obj):
        comments_publication = Comment.objects.filter(publication=obj)
        serializer = CommentSerializer(comments_publication, many=True)

        return serializer.data

    class Meta:
        model = Publication
        fields = ("id", "image", "text", "public", "likes", "comments", "created_at")


class PublicationTimeLineSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_likes(self, obj):
        likes_publication = Like.objects.filter(publication=obj)
        serializer = LikeSerializer(likes_publication, many=True)

        return serializer.data

    def get_comments(self, obj):
        comments_publication = Comment.objects.filter(publication=obj)
        serializer = CommentSerializer(comments_publication, many=True)

        return serializer.data

    class Meta:
        model = Publication
        fields = ("id", "image", "text", "user",
                  "likes", "comments", "created_at")
