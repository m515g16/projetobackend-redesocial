from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("usuarios/list/", views.ListUsuario.as_view()),
    path("usuarios/create/", views.CreateUsuario.as_view()),
    path("usuarios/ret-upd-des/<int:pk>/", views.RetrieveUpdateDestroyUsuario.as_view()),
    path("usuarios/list-follow/", views.ListFollowUsuario.as_view()),
    path("usuarios/create-follow/", views.FollowUsuario.as_view()),
    path("usuarios/delete-follow/<int:pk>/", views.DeleteFollowUsuario.as_view()),
    path("usuarios/friend/", views.FriendUsuario.as_view()),
    path("usuarios/friend/<int:pk>/", views.UpdateFriendUsuario.as_view()),
    path("usuarios/friend/<int:pk>/", views.DeleteFriendUsuario.as_view()),
    path("usuarios/login/", jwt_views.TokenObtainPairView.as_view()),
    path("usuarios/refresh/", jwt_views.TokenRefreshView.as_view()),
]
