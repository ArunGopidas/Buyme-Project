from random import choices

from django.db import models
from core.models import User, SubCategory

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    shopname = models.CharField(max_length=255,unique=True)
    shop_slug = models.SlugField(unique=True)
    website = models.URLField(blank=True,null=True,unique=True)
    category = models.CharField(max_length=200)
    gst_number = models.CharField(max_length=50,unique=True)
    pan_number = models.CharField(max_length=50,unique=True)
    bank_account_number = models.CharField(max_length=50,unique=True)
    ifsc_code = models.CharField(max_length=20,unique=True)
    business_address = models.TextField()
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES=[
        ("APPROVED",'approved'),
        ("PENDING","pending"),
        ("REJECTED",'rejected')
    ]
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="PENDING")
    rejection_reason=models.TextField(blank=True,null=True)

class Product(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name="products")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,default="temp-slug")
    description = models.TextField()
    brand = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    is_cancellable = models.BooleanField(default=True)
    is_returnable = models.BooleanField(default=True)
    return_days = models.IntegerField(default=7)
    approval_status = models.CharField(max_length=20, choices=(('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')), default='PENDING')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sku_code = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(null=True,blank=True)
    tax_percentage = models.FloatField()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)

class InventoryLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    change_amount = models.IntegerField()
    reason = models.CharField(max_length=50)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)