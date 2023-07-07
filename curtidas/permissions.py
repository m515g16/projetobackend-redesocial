from rest_framework.permissions import BasePermission


class LikePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return request.user == obj.user
