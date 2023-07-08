from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from publicacoes.models import Publication
from .serializers import LikeSerializer, LikeUserSerializer
from .permissions import LikePermission
from .models import Like


class LikeListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get(self, request, *args, **kwargs):
        publication_id = kwargs.get("publication_id")
        publication_like = Like.objects.filter(publication_id=publication_id)
        self.queryset = publication_like

        return self.list(request, *args, **kwargs)


class LikeRetrieveUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        publication_like = kwargs.get("publication_id")
        like_user = Like.objects.filter(
            publication_id=publication_like, user_id=user_id).first()

        if not like_user:
            return Response({"detail": "User has no like the publication"}, status=404)

        serializer = LikeUserSerializer(like_user)

        return Response(data=serializer.data, status=200)


class LikeCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Like
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        serializer = LikeSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = request.user
        publication_id = serializer.validated_data.get("publication_id")

        if not Publication.objects.filter(pk=publication_id).exists():
            return Response({"detail": "Not found publication."}, status=404)

        if Like.objects.filter(user=user, publication_id=publication_id).exists():
            return Response({"detail": "User already liked the post."}, status=400)

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        publication_id = serializer.validated_data.get("publication_id")

        return serializer.save(user=user, publication_id=publication_id)


class LikeDestroyView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [LikePermission]
    queryset = Like
    serializer_class = LikeSerializer
