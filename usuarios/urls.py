from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("usuarios/create/", views.CreateUsuario.as_view()),
    path("usuarios/list/", views.RetrieveUsuario.as_view()),
    path("usuarios/update/", views.UpdateUsuario.as_view()),
    path("usuarios/delete/", views.DestroyUsuario.as_view()),
    path("usuarios/login/", jwt_views.TokenObtainPairView.as_view()),
    path("usuarios/refresh/", jwt_views.TokenRefreshView.as_view()),
]
