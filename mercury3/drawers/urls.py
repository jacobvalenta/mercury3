from django.urls import path

from .views import DrawerListView, OpenDrawerView, CloseDrawerView

urlpatterns = [
    path('', DrawerListView.as_view(), name="list"),
    path('open/', OpenDrawerView.as_view(), name="open"),
    path('<int:pk>/close/', CloseDrawerView.as_view(), name="close"),
]
