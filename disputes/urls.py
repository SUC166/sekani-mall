from django.urls import path
from . import views

urlpatterns = [
    path('raise/<int:order_id>/', views.raise_dispute, name='raise_dispute'),
]
