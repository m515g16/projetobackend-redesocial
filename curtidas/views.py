from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from publicacoes.models import Publication
from .serializers import LikeSerializer
from .models import Like


class LikeView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Like
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        publication_id = serializer.validated_data.get("publication_id")

        return serializer.save(user=user, publication_id=publication_id)
