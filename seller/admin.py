from django.contrib import admin
from .models import (
    SellerProfile,
    Product,
    ProductImage,
    InventoryLog,
    SellerEditRequest
)

admin.site.register(SellerProfile)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(InventoryLog)
admin.site.register(SellerEditRequest)