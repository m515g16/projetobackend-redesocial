from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("usuarios/list/", views.ListUsuario.as_view()),
    path("usuarios/create/", views.CreateUsuario.as_view()),
    path("usuarios/ret-upd-des/<int:pk>/", views.RetrieveUpdateDestroyUsuario.as_view()),
    path("usuarios/follow/", views.FollowUsuario.as_view()),
    path("usuarios/friend-request/", views.RetrieveUpdateDestroyUsuario.as_view()),
    path("usuarios/login/", jwt_views.TokenObtainPairView.as_view()),
    path("usuarios/refresh/", jwt_views.TokenRefreshView.as_view()),
]
