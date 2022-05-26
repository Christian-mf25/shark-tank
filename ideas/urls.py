from django.urls import path

from ideas.views import IdeaOwnerView, IdeasView

urlpatterns = [
    path('idea/', IdeasView.as_view()),
    path('ideas/', IdeasView.as_view()),
    path('idea/<idea_id>/', IdeasView.as_view()),
    path('ideas/owner/', IdeaOwnerView.as_view()),
    path('idea/owner/<idea_id>/', IdeaOwnerView.as_view()),
]
