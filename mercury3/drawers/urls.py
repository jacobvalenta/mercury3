from django.urls import path

from .views import OpenDrawerView

urlpatterns = [
    path('open/', OpenDrawerView.as_view(), name="open"),
]
