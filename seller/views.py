

from django.shortcuts import render,redirect
from core.models import User
from seller.decorators import seller_required
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
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        print(first_name, last_name, email, phone_number, password, confirm_password)
        if not all([first_name, last_name, email, phone_number, password, confirm_password]):

            return render(request, "seller/register.html", {"error": "All fields are required"})

        if password != confirm_password:
            return render(request, "seller/register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            return render(request, "seller/register.html", {
                "error": " This email is already registered as a user."
            })
        user = User.objects.create_user(
            username=email.strip().lower(),
            email=email.strip().lower(),
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role="SELLER"
        )
        return redirect("login")

    return render(request, "seller/register.html")



@login_required
def seller_profile(request):

    seller = SellerProfile.objects.filter(user=request.user).first()

    if not seller:
        if request.method == "POST":
            seller = SellerProfile.objects.create(
                user=request.user,
                shopname=request.POST.get("shopname"),
                category=request.POST.get("category"),
                website=request.POST.get("website"),
                gst_number=request.POST.get("gst_number"),
                pan_number=request.POST.get("pan_number").upper(),
                bank_account_number=request.POST.get("bank_account_number"),
                ifsc_code=request.POST.get("ifsc_code"),
                business_address=request.POST.get("business_address"),
                status="PENDING"
                )
            print(seller)
            if seller.shopname:
                seller.shop_slug = slugify(seller.shopname)
                seller.save()

            if request.FILES.get("profile_image"):
                request.user.profile_image = request.FILES.get("profile_image")
                request.user.save()

            return redirect("pending_approval")
        return render(request, "seller/seller_profile.html")

    if seller.status == "REJECTED":
        return redirect("rejected_page")

    if seller.status == "PENDING":
        return redirect("pending_approval")
    return render(request, "seller/seller_profile.html",{"seller":seller})



 
@seller_required
def seller_dashboard(request):
    seller=request.user.seller_profile
    products=Product.objects.filter(seller=seller)
    pending_products = products.filter(approval_status="PENDING").count()
    recent_products=products.order_by("-created_at")
    total_items=products.count()
    context={
        "products":products,
        "total_items":total_items,
        "recent_products":recent_products,
        "pending_products":pending_products
    }
    return render(request, "seller/seller_dashboard.html",context)

@seller_required
def view_seller_profile(request):
    seller=SellerProfile.objects.filter(user=request.user).first()
    return render(request,"seller/seller_profile_view.html",{"seller":seller})

@seller_required
def seller_profile_edit(request):
    seller=request.user.seller_profile

    if seller.status !="APPROVED":
        return redirect("pending_approval")

    if request.method == "POST":
        seller.shopname = request.POST.get('shopname')
        seller.website = request.POST.get('website')
        seller.category = request.POST.get('category')
        seller.business_address=request.POST.get('business_address')
        seller.shop_slug=request.POST.get("shop_slug")
        seller.save()

        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number=request.POST.get('phone_number')
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES.get('profile_image')
        user.save()
        return redirect('view_profile')
    return render(request,'seller/edit_profile.html',{"seller":seller})


@login_required
def pending_approval(request):
    seller=request.user.seller_profile
    if seller.status == "APPROVED":
        return redirect('seller_dashboard')
    return render(request,'seller/Seller_profile_review.html',{"seller":seller})


@seller_required
def add_product(request):

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
        stock_quantity = request.POST.get("stock_quantity")
        is_returnable = True if request.POST.get("is_returnable") == 'on' else False
        is_cancellable = True if request.POST.get("is_cancellable") == 'on' else False
        return_days=request.POST.get("return_days",5)



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
            sku_code=sku,
            price=price,
            selling_price=selling_price,
            cost_price=cost_price,
            stock_quantity=stock_quantity,
            tax_percentage=tax_percentage,
            is_returnable=is_returnable,
            is_cancellable=is_cancellable,
            return_days=return_days,
        )

        images = request.FILES.getlist("images")
        for index, img in enumerate(images)  :
            ProductImage.objects.create(
                product=product,
                image=img,
                is_primary = True if (index == 0 )  else False
            )
        print(request.files)
        return redirect("inventory_page")

    subcategories = SubCategory.objects.all()

    return render(request, "seller/add_product.html", {"subcategories": subcategories})
        

@seller_required
def inventory_page(request):
    products = Product.objects.filter(seller=request.user.seller_profile)
    active_products=products.filter(approval_status="APPROVED").count()
    pending_products=products.filter(approval_status="PENDING").count()
    out_of_stock=products.filter(stock_quantity=0).distinct().count()
    context={
        "products": products,
        "active_products": active_products,
        "pending_products": pending_products,
        "out_of_stock": out_of_stock
    }
    return render(request, "seller/inventory_page.html",context)

@seller_required
def edit_product(request,id):

    product=Product.objects.get(id=id,seller=request.user.seller_profile)

    if request.method =="POST":
        #updating products
        product.name = request.POST.get('name')
        product.description=request.POST.get('description')
        product.brand = request.POST.get('brand')
        product.model_number = request.POST.get('model_number')
        subcategory_id = request.POST.get("subcategory")
        if subcategory_id:
            product.subcategory = SubCategory.objects.get(id=subcategory_id)

        if request.FILES.get("image"):
            product.image=request.FILES.get("image")

        product.sku_code = request.POST.get('sku_code')
        product.stock  = request.POST.get('stock')

        product.slug = slugify(product.name + "-" + product.sku)
        product.price = request.POST.get('price')
        product.selling_price = request.POST.get('selling_price')
        product.cost_price = request.POST.get('cost_price')
        product.tax_percentage = request.POST.get('tax_percentage',5)
        product.is_returnable = True if request.POST.get("is_returnable") == 'on' else False
        product.is_cancellable = True if request.POST.get("is_cancellable") == 'on' else False
        product.save()

        new_image=request.FILES.getlist("images")
        for img in new_image:
            ProductImage.objects.create(
                product=product,
                image=img,
                is_primary=False
            )
        primary_image=request.POST.get('primary_image_id')
        if primary_image:
            product.images.get

        return redirect('inventory_page')
    subcategories=SubCategory.objects.all()
    data={
        "product":product,
        "subcategories":subcategories
    }
    return render(request,'seller/edit_product.html',data)


@seller_required
def delete_product(request,id):
    data=Product.objects.get(id=id,seller=request.user.seller_profile)
    data.delete()
    return redirect('inventory_page')


@seller_required
def customer_dashboard(request):
    return render(request, "customer/dashboard.html")


    
@seller_required
def analytics_page(request):
    return render(request,"seller/analytics_page.html")



@seller_required
def order_page(request):
    order=Order.objects.all(seller=request.user.seller_profile)
    return render(request,"seller/order_page.html",{'orders':order})



@seller_required
def product_preview(request,id,slug):
    seller=request.user.seller_profile
    product=Product.objects.get(id=id,seller=seller)
    images=product.images.all()
    context={
        "product":product,
        "images":images
    }
    return render(request,"seller/product_preview.html",context)



@seller_required
def pending_products(request):
    seller=request.user.seller_profile
    pending_product=Product.objects.filter(seller=seller,approval_status="PENDING").order_by("-id")
    return render(request,"seller/pending_products.html",{"pending_products":pending_product})





