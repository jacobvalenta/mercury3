from django.urls import path

from .views import EmployeeManagementView, EmployeeCreateView

urlpatterns = [
    # path('create_in/', InTransactionCreateView.as_view(), name="create-in"),
    # path('create_out/', OutTransactionCreateView.as_view(), name="create-out"),
    # path('pay/', PayOrRedeemPawnView.as_view(), kwargs={"type": "pay"}, name="pay"),
    # path('redeem/', PayOrRedeemPawnView.as_view(), kwargs={"type": "redeem"}, name="redeem"),
    path('', EmployeeManagementView.as_view(), name="manage"),
    path('create/', EmployeeCreateView.as_view(), name="create"),
]
