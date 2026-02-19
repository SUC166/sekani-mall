from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('verify/<int:order_id>/', views.verify_payment, name='verify_payment'),
    path('webhook/', views.flutterwave_webhook, name='flutterwave_webhook'),
    path('release-escrow/<int:order_id>/', views.release_escrow, name='release_escrow'),
]
