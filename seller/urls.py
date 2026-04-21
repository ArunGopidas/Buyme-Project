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
    path("view_seller_profile", views.view_seller_profile, name="view_profile"),
    path("coupon_page",views.coupon_page,name='coupons_page'),
    path("product_management",views.product_management,name='product_management'),
    path("load_subcategories/", views.load_subcategories, name="load_subcategories"),
    path("change_password/", views.change_password, name="change_password"),
    path("request_edit/", views.request_edit_field, name="request_edit_field"),
    path("update_stock/<int:id>/", views.update_stock, name="update_stock"),
    path("toggle_product_visibility/<int:id>/", views.toggle_product_visibility, name="toggle_product_visibility"),
    path('load_subcategories/<int:id>/', views.load_subcategories, name='load_subcategories'),
    path('primary_image/<int:id>/', views.primary_image, name='primary_image'),
    path('rejected_products', views.rejected_products, name='rejected_products'),
    path('rejected_product_preview/<int:id>/<slug:slug>/', views.product_rejection_view, name='rejected_product_preview'),

    path('delete_product_image/<int:id>/', views.delete_product_image, name='delete_product_image'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)