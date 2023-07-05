from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from usuarios.models import Followers
from .models import Publication
from .serializers import PublicationSerializer, PublicationUserSerializer, PublicationTimeLineSerializer
from .permission import PublicationPermission, PublicationUserPermission
from .pagination import PublicationUserPagination


class PublicationView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [PublicationPermission]
    queryset = Publication.objects.filter(public=True).order_by("created_at")
    serializer_class = PublicationSerializer
    pagination_class = PublicationUserPagination

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
    permission_classes = [PublicationUserPermission]
    serializer_class = PublicationUserSerializer
    pagination_class = PublicationUserPagination

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        publications_user = Publication.objects.filter(
            user_id=user_id).order_by("created_at")

        if not publications_user:
            return Response({"detail": "Not found"}, status=404)

        self.queryset = publications_user

        return self.list(request, *args, **kwargs)


class PublicationTimeLineView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PublicationTimeLineSerializer
    pagination_class = PublicationUserPagination

    def get(self, request, *args, **kwargs):
        user = request.user
        following = Followers.objects.filter(follower=user)
        following_id = []

        if not following:
            return Response({"detail": "Not found"}, status=404)

        for follower in following:
            following_id.append(follower.user_id)

        time_line = Publication.objects.filter(
            user_id__in=following_id).order_by("-created_at")

        self.queryset = time_line

        return self.list(request, *args, **kwargs)
