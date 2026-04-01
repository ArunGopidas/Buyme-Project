from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.seller_register, name='register'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller_profile/',views.seller_profile, name='seller_profile'),
    path('analytics_page/',views.analytics_page,name='analytics_page'),
    path('inventory_page/',views.inventory_page,name='inventory_page'),
    path('order_page/',views.order_page,name='order_page'),
    path('add_product/',views.add_product,name='add_product'),
    path("edit_product/<int:id>/",views.edit_product,name="edit_product"),
    path("delete_product/<int:id>/",views.delete_product,name='delete_product'),
    path("product_preview/<int:id>/<slug:slug>/",views.product_preview,name='product_preview'),
    path("pending_products",views.pending_products,name="pending_products_list"),
    path("pending_approval",views.pending_approval,name="pending_approval"),
    path("edit_seller_profile", views.seller_profile_edit, name="edit_profile"),
    path("view_seller_profile", views.view_seller_profile, name="view_profile")

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)