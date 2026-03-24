from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('customer_register/', views.customer_register, name='customer_register'),
    path('customer_profile/', views.customerprofile, name='customer_profile'),
    #----------------------------------------------------------------------------
    path('customerorder/',views.customerorder,name="customer_order"),
    path('customerwishlist/',views.customerwishlist,name="customer_wishlist"),
    path('customersettings/',views.customersettings,name="customer_settings"),
    path('productlist/',views.productlist,name="productlist"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)