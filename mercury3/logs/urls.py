from django.urls import path

from .views import LogListView

urlpatterns = [
    path('', LogListView.as_view(), name="list"),
    # path('employee/<int:pk>', LogListEmployeeView.as_view(), name="list-employee"),   
]
