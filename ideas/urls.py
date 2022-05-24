from django.urls import path

from ideas.views import IdeasView

urlpatterns = [
    path('idea/', IdeasView.as_view()),
    path('ideas/', IdeasView.as_view()),
    path('idea/<idea_id>/', IdeasView.as_view())
]