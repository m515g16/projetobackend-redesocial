from rest_framework import permissions
from .models import User
from rest_framework.views import View


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj == request.user

class IsFollowOwner(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return  obj.follower == request.user
        
    
class FriendPemission(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return  obj.friend == request.user or obj.user == request.user
        return obj.user == request.user
    
class ListUsersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_staff

        return True