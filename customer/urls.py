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
    path('productcollection/',views.productcollection,name="productcollection"),
    path('productcategory/',views.productcategory,name="productcategory"),
    path('singleproduct/<int:id>/',views.singleproduct,name="singleproduct"),
    path('addcart/<int:id>/',views.addcart,name="addcart"),
    path('cartview/',views.cartview,name="cartview"),
    path('removecart/<int:id>/',views.removecart,name="removecart"),
    path('wishlist/<int:id>/',views.wishlist,name="wishlist"),
    path('wishlistview/',views.wishlistview,name="wishlistview"),
    path('removewishlist/<int:id>/',views.removewishlist,name="removewishlist"),
    path('customeraddress/',views.customer_address,name="customeraddress"),
    path('checkout/',views.checkout,name="checkout"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)