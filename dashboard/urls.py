from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('orders/', views.dashboard_orders, name='dashboard_orders'),
    path('orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('disputes/', views.dashboard_disputes, name='dashboard_disputes'),
    path('discounts/', views.dashboard_discounts, name='dashboard_discounts'),
    path('discounts/add/', views.add_discount, name='add_discount'),
]
