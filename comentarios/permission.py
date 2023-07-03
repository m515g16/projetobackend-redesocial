from rest_framework.permissions import BasePermission, SAFE_METHODS


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated


class CommentUpdateDestroyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
