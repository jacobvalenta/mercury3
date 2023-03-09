from django.urls import path

from .views import TransactionCreateView, TransactionDetailView, InTransactionCreateView

urlpatterns = [
    path('create/', TransactionCreateView.as_view(), name="create-out-zero-info"),
    path('create_in/', InTransactionCreateView.as_view(), name="create-in-zero-info"),
    path('<int:pk>/', TransactionDetailView.as_view(), name="detail"),
    # path('customers/<int:customer_pk>/', CustomerDetailView.as_view(), name="customer-detail"),
    # path('search/', CustomerSearchView.as_view(), name="customer-search")
]
