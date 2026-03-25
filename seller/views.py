from email.policy import default

from django.shortcuts import render,redirect
from core.models import User
from django.contrib.auth.decorators import login_required

from customer.models import Order
from .models import SellerProfile
from .models import Product,ProductImage
from core.models import SubCategory
from django.utils.text import slugify


def seller_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        profile_image=request.FILES.get("profile_image")

        if not all([first_name, last_name, email, phone, password, confirm_password]):
            return render(request, "seller/register.html", {"error": "All fields are required"})

        if password != confirm_password:
            return render(request, "seller/register.html", {"error": "Passwords do not match"})
        
        if User.objects.filter(email=email).exists():
            return render(request, "seller/register.html", {"error": "Email already registered"})
        
        user = User.objects.create_user(
            username=email.strip().lower(),
            email=email.strip().lower(),
            password=password,
            first_name=first_name,
            last_name=last_name,
            profile_image=profile_image,
            role="SELLER"
        )
        user.save()
        return redirect("login")

    return render(request, "seller/register.html")



@login_required
def seller_profile(request):
    if request.user.role != "SELLER":
        return redirect("login")
    profile,created=SellerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.shopname = request.POST.get("shopname")
        profile.category=request.POST.get("category")
        profile.website=request.POST.get("website")
        profile.gst_number =request.POST.get("gst_number")
        profile.pan_number =request.POST.get("pan_number")
        profile.bank_account_number =request.POST.get("bank_account_number")
        profile.ifsc_code  =request.POST.get("ifsc_code")
        profile.business_address =request.POST.get("business_address")
        if request.FILES.get("profile_image"):
            request.user.profile_image =request.FILES.get("profile_image")
            request.user.save()
        profile.save()
        return redirect("seller_dashboard")
    return render(request,"seller/sellerprofile.html",{"profile":profile})


 
@login_required
def seller_dashboard(request):
    if request.user.role != "SELLER":
        return redirect("login")
    seller=request.user.seller_profile
    products=Product.objects.filter(seller=seller)
    pending_products = products.filter(approval_status="PENDING").count()
    recent_products=products.order_by("-created_at")
    return render(request,"seller/seller_dashboard.html",{
        "products":products,
        "recent_products":recent_products,
        "pending_products":pending_products
    })


@login_required
def addproduct(request):

    if request.user.role != "SELLER":
        return redirect("login")

    seller =SellerProfile.objects.get(user=request.user)

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        brand = request.POST.get("brand")
        model_number = request.POST.get("model_number")
        subcategory_id = request.POST.get("subcategory")
        sku = request.POST.get("sku")
        price = request.POST.get("price")
        selling_price=request.POST.get('selling_price')
        cost_price=request.POST.get('cost_price')
        tax_percentage=request.POST.get('tax_percentage',5)
        stock_quantity = request.POST.get("stock")
        weight = request.POST.get("weight", 0)
        length = request.POST.get("length", 0)
        width = request.POST.get("width", 0)
        height = request.POST.get("height", 0)
        is_returnable = True if request.POST.get("is_returnable") == 'on' else False
        is_cancellable = True if request.POST.get("is_cancellable") == 'on' else False
        return_days=request.POST.get("return_days",5)
        image = request.FILES.get("image")

        subcategory = SubCategory.objects.get(id=subcategory_id)

        slug = slugify(name + "-" + sku) 

        product = Product.objects.create(
            seller=seller,
            subcategory=subcategory,
            name=name,
            slug=slug,
            description=description,
            brand=brand,
            model_number=model_number,
            image=image,
            sku_code=sku,
            price=price,
            selling_price=selling_price,
            cost_price=cost_price,
            stock_quantity=stock_quantity,
            weight=weight,
            length=length,
            width=width,
            height=height,
            tax_percentage=tax_percentage,
            is_returnable=is_returnable,
            is_cancellable=is_cancellable,
            return_days=return_days
        )


        if image:
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=True
            )

        return redirect("inventory_page")

    subcategories = SubCategory.objects.all()

    return render(request, "seller/addproduct.html", {"subcategories": subcategories})
        

@login_required
def inventorypage(request):
    seller =request.user.seller_profile
    products = Product.objects.filter(seller=seller)
    active_products=products.filter(approval_status="APPROVED").count()
    pending_products=products.filter(approval_status="PENDING").count()
    out_of_stock=products.filter(stock_quantity=0).distinct().count()
    context={
        "products": products,
        "active_products": active_products,
        "pending_products": pending_products,
        "out_of_stock": out_of_stock
    }
    return render(request, "seller/inventorypage.html",context)

@login_required
def edit_product(request,id):
    if request.user.role != "SELLER":
        return redirect('login')

    seller=request.user.seller_profile

    product=Product.objects.get(id=id,seller=seller)

    if request.method =="POST":
        #updating products
        product.name = request.POST.get('name')
        product.description=request.POST.get('description')
        product.brand = request.POST.get('brand')
        product.model_number = request.POST.get('model_number')
        subcategory_id = request.POST.get("subcategory")
        product.subcategory = SubCategory.objects.get(id=subcategory_id)
        product.image=request.FILES.get("image")
        product.sku = request.POST.get('sku')
        product.stock  = request.POST.get('stock')
        product.slug = slugify(product.name + "-" + product.sku)
        product.price = request.POST.get('price')
        product.selling_price = request.POST.get('selling_price')
        product.cost_price = request.POST.get('cost_price')
        product.tax_percentage = request.POST.get('tax_percentage',5)
        product.weight = request.POST.get("weight")
        product.length = request.POST.get("length")
        product.width = request.POST.get("width")
        product.height = request.POST.get("height")
        product.is_returnable = True if request.POST.get("is_returnable") == 'on' else False
        product.is_cancellable = True if request.POST.get("is_cancellable") == 'on' else False
        product.save()

        new_image=request.FILES.get("image")
        if new_image:
            ProductImage.objects.create(
                product=product,
                image=new_image
            )
        return redirect('inventory_page')
    subcategories=SubCategory.objects.all()
    data={
        "product":product,
        "subcategories":subcategories
    }
    return render(request,'seller/editproduct.html',data)


@login_required
def delete_product(request,id):
    if request.user.role != "SELLER":
        return redirect("login")
    else:
        data=Product.objects.get(id=id)
        data.delete()
    return redirect('inventory_page')

def customer_dashboard(request):
    return render(request, "customer/dashboard.html")
    
    
def analyticspage(request):
    return render(request,"seller/analyticspage.html")


def orderpage(request):
    if request.user.role != "SELLER":
        return redirect("login")
    order=Order.objects.all()
    return render(request,"seller/orderpage.html",{'orders':order})



def product_preview(request,id):
    if request.user.role != 'SELLER':
        return redirect('login')
    seller=request.user.seller_profile
    product=Product.objects.get(id=id,seller=seller)
    images=product.images.all()
    context={
        "product":product,
        "images":images
    }
    return render(request,"seller/product_preview.html",context)

def pending_products(request):
    if request.user.role != "SELLER":
        return redirect("login")
    seller=request.user.seller_profile
    pending_product=Product.objects.filter(seller=seller,approval_status="PENDING").order_by("-id")
    return render(request,"seller/pending_products.html",{"pending_products":pending_product})