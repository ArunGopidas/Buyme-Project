from django.urls import path
from . import views
from seller import views as seller_views

urlpatterns = [
    path("login/",views.login_view,name="login"),
    path('seller/dashboard/', seller_views.seller_dashboard, name='seller_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

   
]