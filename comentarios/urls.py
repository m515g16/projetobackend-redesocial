from django.urls import path
from .views import CommentView, CommentUpdateDestroyView

urlpatterns = [
    path("", CommentView.as_view()),
    path("<int:id>/", CommentUpdateDestroyView.as_view())
]
