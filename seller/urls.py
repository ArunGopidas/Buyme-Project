from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.seller_register, name='register'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller_profile/',views.seller_profile, name='seller_profile'),
    path('analytics_page/',views.analyticspage,name='analytics_page'),
    path('inventory_page/',views.inventorypage,name='inventory_page'),
    path('order_page/',views.orderpage,name='order_page'),
    path('add_product/',views.addproduct,name='add_product'),
    path("edit_product/<int:id>/",views.edit_product,name="edit"),
    path("delete_product/<int:id>/",views.delete_product,name='delete_product'),
    path("product_preview/<int:id>/",views.product_preview,name='product_preview')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)