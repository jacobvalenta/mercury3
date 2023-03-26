from django.urls import path

from .views import (ItemSearchView, ItemDetailView, SetItemLocationView,
                    LocationAssignmentView, MoveItemToBucketView,
                    RemoveItemFromBucketView,
                    InventoryAuditView, InventoryAuditDetailView,
                    audit_scan_item_view, audit_finish, audit_reopen_view,
                    audit_make_missing_items_view,
                    search_item_number_ajax_view)

urlpatterns = [
    path('search/', ItemSearchView.as_view(), name="search"),
    path('location_assignment/', LocationAssignmentView.as_view(),
         name="location-assignment"),
    path('<int:pk>/', ItemDetailView.as_view(), name="detail"),
    path('<int:pk>/set_location/', SetItemLocationView.as_view(),
         name="set-location"),
    path('<int:pk>/move_to_bucket/', MoveItemToBucketView.as_view(),
         name="move-to-bucket"),
    path('<int:pk>/remove_from_bucket/', RemoveItemFromBucketView.as_view(),
         name="remove-from-bucket"),

    # Audits
    path('audit/', InventoryAuditView.as_view(), name="inventory-audit"),
    path('audit/done/', audit_finish, name="inventory-audit-done"),
    path('audit/scan/', audit_scan_item_view,
         name="inventory-audit-scan"),
    path('audit/<int:pk>/', InventoryAuditDetailView.as_view(),
         name="inventory-audit-detail"),
    path('audit/<int:pk>/reopen/', audit_reopen_view,
         name="inventory-audit-reopen"),
    path('audit/<int:pk>/make_missing_items/', audit_make_missing_items_view,
         name="inventory-audit-make-missing-items"),

    # Ajax views
    path('search/simple/',
         search_item_number_ajax_view,
         name="item-search-simple-ajax")
]
