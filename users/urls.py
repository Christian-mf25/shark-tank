from django.urls import path

from .views import UserDetailsView, UserView, login

urlpatterns = [
    path("users/", UserView.as_view()),
    path("users/<uuid>/", UserDetailsView.as_view()),
    path("login/", login),
]
