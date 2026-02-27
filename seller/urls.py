from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.seller_register, name='seller_register'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    
]