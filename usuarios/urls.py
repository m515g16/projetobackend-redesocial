from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    
    path("usuarios/", views.ListCreateUsuario.as_view()),
    path("usuarios/<int:pk>/",
         views.RetrieveUpdateDestroyUsuario.as_view()),

    path("usuarios/follow/list/", views.ListFollow.as_view()),
    path("usuarios/follow/", views.FollowUsuario.as_view()),
    path("usuarios/follow/<int:pk>/", views.DeleteFollowUsuario.as_view()),

    path("usuarios/friend/", views.FriendUsuario.as_view()),
    path("usuarios/friend/<int:pk>/", views.RetriveUpdateDestroyFriendUsuario.as_view()),

    path("usuarios/login/", jwt_views.TokenObtainPairView.as_view()),
    path("usuarios/refresh/", jwt_views.TokenRefreshView.as_view()),
]
