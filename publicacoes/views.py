from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from usuarios.models import Followers, FriendSolicitations
from .models import Publication
from .serializers import PublicationSerializer, PublicationUserSerializer, PublicationTimeLineSerializer
from .permission import PublicationPermission, PublicationUserPermission
from .pagination import PaginationCustomer


class PublicationView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [PublicationPermission]
    queryset = Publication.objects.filter(public=True).order_by("created_at")
    serializer_class = PublicationSerializer
    pagination_class = PaginationCustomer

    def perform_create(self, serializer):
        user = self.request.user
        publication = serializer.save(user=user)

        return publication


class PublicationRetrieveView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [PublicationUserPermission]
    queryset = Publication
    serializer_class = PublicationSerializer


class PublicationUserView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PublicationUserSerializer
    pagination_class = PaginationCustomer

    def get(self, request, *args, **kwargs):
        user = request.user
        user_publication = kwargs.get("user_id")
        follower = Followers.objects.filter(
            user_id=user_publication, follower=user).first()
        friend_user = FriendSolicitations.objects.filter(
            user=user, friend_id=user_publication).first()
        user_friend = FriendSolicitations.objects.filter(
            friend=user, user_id=user_publication).first()

        if friend_user or user_friend or follower:
            publications_user = Publication.objects.filter(
                user_id=user_publication).order_by("created_at")

        if not friend_user and not user_friend and not follower:
            publications_user = Publication.objects.filter(
                user_id=user_publication, public=True).order_by("created_at")

        if not publications_user:
            return Response({"detail": "Not found"}, status=404)

        self.queryset = publications_user

        return self.list(request, *args, **kwargs)


class PublicationTimeLineView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PublicationTimeLineSerializer
    pagination_class = PaginationCustomer

    def get(self, request, *args, **kwargs):
        user = request.user
        following = Followers.objects.filter(follower=user)
        friend_user = FriendSolicitations.objects.filter(user=user, accepted=True)
        user_friend = FriendSolicitations.objects.filter(friend=user, accepted=True)
        friends = [*friend_user, *user_friend]
        following_friends = []

        if not following and not friends:
            return Response({"detail": "Not found"}, status=404)

        for follower in following:
            following_friends.append(follower.user_id)

        for friend in friends:
            if friend.user_id != user.id:
                following_friends.append(friend.user_id)
            else:
                following_friends.append(friend.friend_id)

        time_line = Publication.objects.filter(
            user_id__in=following_friends).order_by("-created_at")

        self.queryset = time_line

        return self.list(request, *args, **kwargs)
