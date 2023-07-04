from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.serializers import ValidationError
from .permission import CommentPermission, CommentUpdateDestroyPermission
from .models import Comment
from .serializers import CommentSerializer


class CommentView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CommentPermission]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        publication_id = serializer.validated_data["publication_id"]

        return serializer.save(user=user, publication_id=publication_id)


class CommentUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CommentUpdateDestroyPermission]
    queryset = Comment
    serializer_class = CommentSerializer
    lookup_field = "id"
