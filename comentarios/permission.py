from rest_framework.permissions import BasePermission, SAFE_METHODS
from usuarios.models import Follower, Friend
from publicacoes.models import Publication
from .serializers import CommentSerializer


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user_id = request.user.id
        serializer = CommentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        publication = serializer.validated_data.get("publication_id")
        publication = Publication.objects.filter(pk=publication).first()

        if publication.public:
            return True

        publication_user_id = publication.user.id
        follower = Follower.objects.filter(
            follower_id=user_id, user_id=publication_user_id)

        if follower:
            return True

        friend = Friend.objects.filter(
            friend_id=user_id, user_id=publication_user_id)

        if friend:
            return True

        return False


class CommentUpdateDestroyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
