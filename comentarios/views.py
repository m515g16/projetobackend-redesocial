from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permission import CommentPermission, CommentUpdateDestroyPermission
from .models import Comment
from .serializers import CommentSerializer


class CommentView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CommentPermission]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        publication_id = serializer.validated_data.get("publication_id")

        return serializer.save(user=user, publication_id=publication_id)


class CommentUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CommentUpdateDestroyPermission]
    queryset = Comment
    serializer_class = CommentSerializer
    lookup_field = "id"
