from django.urls import path

from investments.views import InvestmentsView

urlpatterns = [
    path("investment/", InvestmentsView.as_view()),
]
