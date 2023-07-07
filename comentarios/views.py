from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .pagination import PaginationCustomer
from .permission import CommentPermission, CommentUpdateDestroyPermission
from .models import Comment
from .serializers import CommentSerializer, CommentUserSerializer


class CommentView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CommentPermission]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        publication_id = serializer.validated_data["publication_id"]

        return serializer.save(user=user, publication_id=publication_id)


class CommentPublicationView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationCustomer
    serializer_class = CommentUserSerializer

    def get(self, request, *args, **kwargs):
        publication_id = kwargs.get("publication_id")
        comment = Comment.objects.filter(publication_id=publication_id)
        print(publication_id)

        if not comment:
            return Response({"detail": "Not found publication."}, status=404)

        self.queryset = comment

        return self.list(request, *args, **kwargs)


class CommentUpdateDestroyView(UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CommentUpdateDestroyPermission]
    queryset = Comment
    serializer_class = CommentSerializer
    lookup_field = "id"
