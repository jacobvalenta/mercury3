from django.urls import path

from .views import (EmployeeManagementView, EmployeeCreateView,
                    EmployeeListView, EmployeeDetailView, EmployeeUpdateView)

urlpatterns = [
    path('', EmployeeManagementView.as_view(), name="manage"),
    path('create/', EmployeeCreateView.as_view(), name="create"),
    path('list/', EmployeeListView.as_view(), name="list"),
    path('<int:pk>/', EmployeeDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', EmployeeUpdateView.as_view(), name="update")
]
