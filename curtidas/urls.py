from django.urls import path
from .views import LikeCreateView, LikeDestroyView, LikeListView, LikeRetrieveUserView

urlpatterns = [
    path("", LikeCreateView.as_view()),
    path("<int:pk>/", LikeDestroyView.as_view()),
    path("publication/<int:publication_id>/", LikeListView.as_view()),
    path("publication/<int:publication_id>/user/",
         LikeRetrieveUserView.as_view())
]
