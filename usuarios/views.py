from rest_framework.views import APIView, Request, Response, status
from .models import User, Follower, Friend
from .serializers import UserSerializer, FollowerSerializer, FriendSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwner
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from exceptions import FollowExistsError, FriendshipExistsError



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

    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def post(self, req:Request) -> Response:
            serializer = FollowerSerializer(data=req.data)

            serializer.is_valid(raise_exception=True)

            follower = self.request.user
        
            user_id = self.request.data.get("user_id")
            
            user = User.objects.get(pk=user_id)

            if Follower.objects.filter(user=user, follower=follower).exists():
                print("caiu")
                return Response({'error': 'Usuária já segue essa pessoa'}, status.HTTP_400_BAD_REQUEST)
            
            serializer.save(follower=follower, user=user)
                
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            

class FriendUsuario(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def post(self, req:Request) -> Response:
        serializer = FriendSerializer(data=req.data)

        serializer.is_valid(raise_exception=True)

        friend = self.request.user
        
        user_id = self.request.data.get("user_id")
        
        user = User.objects.get(pk=user_id)
        
        if Friend.objects.filter(user=user, friend=friend).exists():
             return Response ({'error': 'Usuária já é amiga dessa pessoa'}, status.HTTP_400_BAD_REQUEST)   
        
        serializer.save(friend=friend, user=user)
    
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    


        
