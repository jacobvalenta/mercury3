from django.urls import path

from .views import ItemSearchView, ItemDetailView, search_item_number_ajax_view

urlpatterns = [
    path('search/', ItemSearchView.as_view(), name="search"),
    path('<int:pk>/', ItemDetailView.as_view(), name="detail"),

    path('search/simple/', search_item_number_ajax_view, name="item-search-simple-ajax")
]
