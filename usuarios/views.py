from rest_framework.views import APIView, Request, Response, status
from .models import User, Followers, FriendSolicitations, Friends
from .serializers import UserSerializer, FollowerSerializer, FriendSerializer, FriendAnswerSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwner, IsFollowOwner, IsFriendOwner, FriendAnswer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveDestroyAPIView,RetrieveUpdateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication




class ListUsuario(ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateUsuario(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
    
class ListFollowUsuario(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer

class FollowUsuario(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer

    def post(self, req:Request) -> Response:
            serializer = FollowerSerializer(data=req.data)

            serializer.is_valid(raise_exception=True)

            follower = self.request.user
        
            user_id = self.request.data.get("user_id")
            
            user = User.objects.get(pk=user_id)

            if Followers.objects.filter(user=user, follower=follower).exists():
                return Response({'detail': 'Usuária já segue essa pessoa'}, status.HTTP_400_BAD_REQUEST)
            
            if user_id == self.request.user.id:
                return Response({'detail': 'Não pode seguir a si mesmo'}, status.HTTP_400_BAD_REQUEST)
            
            serializer.save(follower=follower, user=user)
                
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class DeleteFollowUsuario(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFollowOwner]

    queryset = Followers.objects.all()
    serializer_class = FollowerSerializer 

      

    def destroy(self, request, *args, **kwargs):
        follower = request.user
        instance = Followers.objects.get(user_id=self.kwargs.get("pk"), follower=follower)
        if not instance:
            return Response({'detail': 'Você não segue esse pessoa ou ela não existe'}, status.HTTP_400_BAD_REQUEST)     
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendUsuario(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    
    serializer_class = FriendSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        list_friends1 = FriendSolicitations.objects.filter(friend=user, accepted=True)
        list_friends2 = FriendSolicitations.objects.filter(user=user, accepted=True)
        list_friends = [*list_friends1, *list_friends2]
        
        self.queryset = list_friends

        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serializer = FriendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user_solicited = serializer.validated_data.get("user_id")
        
        if FriendSolicitations.objects.filter(user_id=user_solicited, friend=user).exists():
            return Response({'detail': 'Usuária já é amigo dessa pessoa'}, status.HTTP_400_BAD_REQUEST)
            
        if user_solicited == request.user.id:
            return Response({'detail': 'Não pode solicitar amizade a si mesmo'}, status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        user = self.request.user
        user_solicited = serializer.validated_data.get("user_id")

        
        return serializer.save(friend=user, user_id=user_solicited)
    
class UpdateFriendUsuario(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = FriendSolicitations.objects.all()
    serializer_class = FriendSerializer

    lookup_url_kwarg = "pk"

    def perform_update(self, serializer):
        user_solicited = self.request.user


        
        friend = FriendSolicitations.objects.get(friend_id=self.kwargs.get("pk"), user_id=user_solicited.id)

        friend_id = friend.friend_id
        
        friend_user = User.objects.get(pk=friend_id)
        
        answer = serializer.validated_data.get("accepted")

        if answer:
            Friends.objects.create(from_user=friend_user, to_user=user_solicited)
            Friends.objects.create(from_user=user_solicited, to_user=friend_user)
        
        return serializer.save(friend=user_solicited, user_id=friend_id)


        


class DeleteFriendUsuario(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsFriendOwner]

    queryset = FriendSolicitations.objects.all()
    serializer_class = FriendSerializer 

    lookup_url_kwarg = "pk"
    


        
