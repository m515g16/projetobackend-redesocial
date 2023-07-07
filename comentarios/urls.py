from django.urls import path
from .views import CommentView, CommentUpdateDestroyView, CommentPublicationView

urlpatterns = [
    path("", CommentView.as_view()),
    path("<int:id>/", CommentUpdateDestroyView.as_view()),
    path("publication/<int:publication_id>/", CommentPublicationView.as_view())
]
