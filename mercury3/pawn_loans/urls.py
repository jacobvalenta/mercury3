from django.urls import path

from .views import PawnLoanDetailView

urlpatterns = [
    path('<int:pk>/', PawnLoanDetailView.as_view(), name="detail"),
]
