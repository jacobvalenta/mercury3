from django.urls import path

from .views import InTransactionCreateView, OutTransactionCreateView, PayOrRedeemPawnView, TransactionDetailView

urlpatterns = [
    path('create_in/', InTransactionCreateView.as_view(), name="create-in"),
    path('create_out/', OutTransactionCreateView.as_view(), name="create-out"),
    path('pay/', PayOrRedeemPawnView.as_view(), kwargs={"type": "pay"}, name="pay"),
    path('redeem/', PayOrRedeemPawnView.as_view(), kwargs={"type": "redeem"}, name="redeem"),
    path('<int:pk>/', TransactionDetailView.as_view(), name="detail"),
]
