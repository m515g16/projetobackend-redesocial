from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from usuarios.models import Follower, Friend


class PublicationPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated


class PublicationUserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.method in SAFE_METHODS:
            return request.user == obj.user

        if obj.public:
            return True

        publication_user_id = obj.user.id
        user_id = request.user.id
        follower = Follower.objects.filter(
            follower_id=user_id, user_id=publication_user_id)

        if follower:
            return True

        friend = Friend.objects.filter(
            friend_id=user_id, user_id=publication_user_id)

        if friend:
            return True

        return False
