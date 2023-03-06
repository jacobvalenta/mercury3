from django.urls import path

from .views import search_item_number_ajax_view

urlpatterns = [
    path('search/simple/', search_item_number_ajax_view, name="item-search-simple-ajax")
]
