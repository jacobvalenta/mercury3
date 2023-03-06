from django.urls import path

from .views import TransactionCreateView

urlpatterns = [
    path('create/', TransactionCreateView.as_view(), name="create-out-zero-info"),
    # path('customers/<int:customer_pk>/', CustomerDetailView.as_view(), name="customer-detail"),
    # path('customers/search/', CustomerSearchView.as_view(), name="customer-search")
]
