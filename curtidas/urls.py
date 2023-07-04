from django.urls import path
from .views import LikeView

urlpatterns = [
    path("", LikeView.as_view()),
]
