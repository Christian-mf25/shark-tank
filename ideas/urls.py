from django.urls import path

from ideas.views import IdeasView

urlpatterns = [
    path('idea/', IdeasView.as_view())
]