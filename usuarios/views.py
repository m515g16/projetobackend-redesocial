from rest_framework.views import Request, Response, status
from .models import User, Followers, FriendSolicitations
from .serializers import UserSerializer, FollowerSerializer, FriendSerializer, UserFriendSerializer, UserFollowersSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwner, IsFollowOwner, FriendPemission, ListUsersPermission
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination




class ListCreateUsuario(ListCreateAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class RetrieveUpdateDestroyUsuario(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)

        if 'password' in request.data:
            password = request.data['password']
            instance.set_password(password)

        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class FollowUsuario(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer

    def post(self, req: Request) -> Response:
        serializer = FollowerSerializer(data=req.data)

        serializer.is_valid(raise_exception=True)

        follower = self.request.user

        user_id = self.request.data.get("user_id")

        user = User.objects.filter(pk=user_id).first()

        if not user:
            return Response(data={'detail': 'User not exists'}, status=status.HTTP_404_NOT_FOUND)

        if Followers.objects.filter(user=user, follower=follower).exists():
            return Response({'detail': 'User already following this person'}, status.HTTP_400_BAD_REQUEST)

        if user_id == self.request.user.id:
            return Response({'detail': 'You cant be follwen yourself'}, status.HTTP_400_BAD_REQUEST)

        serializer.save(follower=follower, user=user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class RetrieveDeleteFollowUsuario(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFollowOwner]

    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = User
        self.serializer_class = UserFollowersSerializer

        return self.retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        follower = request.user
        
        instance = Followers.objects.filter(user_id=self.kwargs.get("pk"), follower=follower).first()

        if not instance:
            return Response({'detail': 'You dont follow this person'}, status.HTTP_404_NOT_FOUND)     
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendUsuario(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FriendSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        list_friends1 = FriendSolicitations.objects.filter(
            friend=user, accepted=True)
        list_friends2 = FriendSolicitations.objects.filter(
            user=user, accepted=True)
        list_friends = [*list_friends1, *list_friends2]

        self.queryset = list_friends

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = FriendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user_solicited = serializer.validated_data.get("user_id")

        user = User.objects.filter(pk=user_solicited).first()
        if not user:
            return Response({'detail': 'User not found'}, status.HTTP_404_NOT_FOUND)

        if FriendSolicitations.objects.filter(user_id=user_solicited, friend=user).exists():
            return Response({'detail': 'You are already friend that person'}, status.HTTP_400_BAD_REQUEST)

        if user_solicited == request.user.id:
            return Response({'detail': 'You cant request friendship yourself'}, status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        user_solicited = serializer.validated_data.get("user_id")

        return serializer.save(friend=user, user_id=user_solicited)


class RetriveUpdateDestroyFriendUsuario(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [FriendPemission]

    queryset = FriendSolicitations.objects.all()
    serializer_class = FriendSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = User
        self.serializer_class = UserFriendSerializer

        return self.retrieve(request, *args, **kwargs)


        
    def update(self, request, *args, **kwargs):
        user=request.user
        friend_id=kwargs.get("pk")
        
        partial = kwargs.pop('partial', False)
        instance = FriendSolicitations.objects.filter(friend_id=friend_id, user=user).first()
        if not instance:
            return Response({'detail': 'Person not found'}, status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    
    



