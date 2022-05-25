from django.urls import path

from .views import UserView, login

urlpatterns = [path("users/", UserView.as_view()), path("login/", login)]
