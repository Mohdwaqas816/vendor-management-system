from django.urls import path
from . import views


urlpatterns = [
    # url endpoint for health check
    path("health/",views.health, name="test_func"),

    # jwt endpoints


    # url endpoints for vendor 
    path('vendors/', views.vendor_list_create, name='vendor-list-create'),
    path('vendors/<str:pk>/', views.vendor_retrieve_update_destroy, name='vendor-retrieve-update-destroy'),
    path('vendors/<str:pk>/performance/', views.vendor_performance, name='vendor-performance'),

    # url endpoints for purchase order
    path('purchase_orders/', views.purchase_order_list_create, name='purchase-order-list-create'),
    path('purchase_orders/<str:pk>/', views.purchase_order_retrieve_update_destroy, name='purchase-order-retrieve-update-destroy'),
    path('purchase_orders/<str:pk>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge-purchase-order'),


]

