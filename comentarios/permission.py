from rest_framework.permissions import BasePermission, SAFE_METHODS
from usuarios.models import Followers, FriendSolicitations
from publicacoes.models import Publication
from .serializers import CommentSerializer


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        serializer = CommentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        publication = serializer.validated_data.get("publication_id")
        publication = Publication.objects.filter(pk=publication).first()

        if publication.public:
            return True

        if not request.user.is_authenticated:
            return False

        publication_user_id = publication.user_id
        follower = Followers.objects.filter(
            follower_id=user_id, user_id=publication_user_id)

        if publication_user_id == user_id:
            return True

        if follower:
            return True

        friend_user = FriendSolicitations.objects.filter(
            friend_id=user_id, user_id=publication_user_id).first()
        user_friend = FriendSolicitations.objects.filter(
            friend_id=publication_user_id, user_id=user_id).first()

        if friend_user or user_friend:
            return True

        return False


class CommentUpdateDestroyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
