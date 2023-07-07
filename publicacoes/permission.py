from rest_framework.permissions import BasePermission, SAFE_METHODS
from usuarios.models import Followers, FriendSolicitations


class PublicationPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated


class PublicationUserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.method in SAFE_METHODS:
            return request.user == obj.user

        if obj.public or request.user == obj.user:
            return True

        publication_user_id = obj.user.id
        user_id = request.user.id
        follower = Followers.objects.filter(
            follower_id=user_id, user_id=publication_user_id).first()

        if follower:
            return True

        friend_user = FriendSolicitations.objects.filter(
            friend_id=user_id, user_id=publication_user_id).first()
        user_friend = FriendSolicitations.objects.filter(
            friend_id=publication_user_id, user_id=user_id).first()

        if friend_user or user_friend:
            return True

        return False
