from django.urls import path
from .views import PublicationView, PublicationRetrieveView, PublicationUserView

urlpatterns = [
    path("", PublicationView.as_view()),
    path("<int:pk>/", PublicationRetrieveView.as_view()),
    path("user/<int:user_id>/", PublicationUserView.as_view()),
]
