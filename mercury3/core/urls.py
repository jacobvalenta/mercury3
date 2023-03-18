from django.contrib.auth.views import LoginView
from django.urls import path

from .views import MainPageView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),

    path('', MainPageView.as_view(), name="main-page")
]
