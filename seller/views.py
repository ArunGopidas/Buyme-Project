from django.shortcuts import render,redirect
from core.models import User
from django.contrib.auth.decorators import login_required
from .models import SellerProfile
from .models import Product,ProductVariant,ProductImage
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
    return render(request,"seller/seller_dashboard.html")


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
        stock = request.POST.get("stock")

        image = request.POST.get("image")

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
        )

        variant = ProductVariant.objects.create(
            product=product,
            sku_code=sku,
            mrp=price,
            selling_price=price,
            cost_price=price,
            stock_quantity=stock,
            weight=1,
            length=1,
            width=1,
            height=1,
            tax_percentage=5
        )


        if image:
            ProductImage.objects.create(
                variant=variant,
                image_url=image
            )

        return redirect("inventorypage")

    subcategories = SubCategory.objects.all()

    return render(request, "seller/addproduct.html", {"subcategories": subcategories})
        

@login_required
def inventorypage(request):
    seller =request.user.seller_profile
    products = Product.objects.filter(seller=seller).order_by("-created_at")
    return render(request, "seller/inventorypage.html", {"products": products})

@login_required
def editproduct(request,id):
  
    if request.user.role != "SELLER":
        return redirect("login")

    seller = request.user.seller_profile

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        brand = request.POST.get("brand")
        model_number = request.POST.get("model_number")
        subcategory_id = request.POST.get("subcategory")

        sku = request.POST.get("sku")
        price = request.POST.get("price")
        stock = request.POST.get("stock")

        image = request.POST.get("image_url")

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
        )

        variant = ProductVariant.objects.create(
            product=product,
            sku_code=sku,
            mrp=price,
            selling_price=price,
            cost_price=price,
            stock_quantity=stock,
            weight=1,
            length=1,
            width=1,
            height=1,
            tax_percentage=5
        )


        if image:
            ProductImage.objects.create(
                variant=variant,
                image_url=image
            )

        return redirect("inventorypage")

    subcategories = SubCategory.objects.all()
    return render(request,"seller/editproduct.html",{"product":product,"variant":variant})

@login_required
def deleteproduct(request,id):
    if request.user.role != "SELLER":
        return redirect("login")
    seller






def customer_dashboard(request):
    return render(request, "customer/dashboard.html")
    
    


def analyticspage(request):
    return render(request,"seller/analyticspage.html")




def orderpage(request):
    return render(request,"seller/orderpage.html")








