from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.customer_login, name='login'),
    path('sekani-login/', views.sekani_admin_login, name='sekani_admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]
