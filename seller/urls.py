from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.seller_register, name='seller_register'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('sellerprofile/',views.seller_profile, name='sellerprofile'),
    path('analyticspage/',views.analyticspage,name='analyticspage'),
    path('inventorypage/',views.inventorypage,name='inventorypage'),
    path('orderpage/',views.orderpage,name='orderpage'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path("editproduct/<int:id>/",views.editproduct,name="editproduct"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)