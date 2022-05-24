from django.urls import path

from ideas.views import IdeasView

urlpatterns = [
    path('ideas/', IdeasView.as_view())
]