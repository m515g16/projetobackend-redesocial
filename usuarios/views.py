from rest_framework.views import APIView, Request, Response, status
from .models import Usuario
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UsuarioSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsAccountOwner
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView


class CreateUsuario(CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class RetrieveUsuario(RetrieveAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    lookup_url_kwarg = "pk"

class UpdateUsuario(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

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

class DestroyUsuario(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    lookup_url_kwarg = "pk"

