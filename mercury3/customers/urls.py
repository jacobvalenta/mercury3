from django.urls import path

from .views import CustomerCreateView, CustomerDetailView, CustomerSearchView

urlpatterns = [
    path('customers/create/', CustomerCreateView.as_view(), name="customer-create"),
    path('customers/<int:customer_pk>/', CustomerDetailView.as_view(), name="customer-detail"),
    path('customers/search/', CustomerSearchView.as_view(), name="customer-search")
]
