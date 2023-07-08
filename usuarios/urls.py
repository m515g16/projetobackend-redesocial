from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    
    path("", views.ListCreateUsuario.as_view()),
    path("<int:pk>/",
         views.RetrieveUpdateDestroyUsuario.as_view()),

    path("follow/", views.FollowUsuario.as_view()),
    path("follow/<int:pk>/", views.RetrieveDeleteFollowUsuario.as_view()),

    path("friend/", views.FriendUsuario.as_view()),
    path("friend/<int:pk>/", views.RetriveUpdateDestroyFriendUsuario.as_view()),

    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("refresh/", jwt_views.TokenRefreshView.as_view()),
]
