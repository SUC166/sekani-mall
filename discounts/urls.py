from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_discount, name='apply_discount'),
]
