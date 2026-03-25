from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import *
from seller.models import *
from customer.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth import login
User = get_user_model()


# Create your views here.
def home_view(request):
    product=Product.objects.filter(approval_status="APPROVED").prefetch_related("images")
    category=Category.objects.all()
    if request.user.is_authenticated:
        return render(request,'customer/home.html',{"products":product,"categories":category})
    return render(request,'customer/home.html',{"products":product,"categories":category})

def customer_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        profile_image = request.FILES.get("profile_image")

        if not first_name or not email or not password:
            messages.error(request, "All fields are required")
            return redirect("customer_register")

        email = email.strip().lower()

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("customer_register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("customer_register")

        if phone and User.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number already exists")
            return redirect("customer_register")

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            user.role = "CUSTOMER"
            user.phone_number = phone
            if profile_image:
                user.profile_image = profile_image
            user.save()
            print('hloo')
            messages.success(request, "Account created successfully")
            return redirect("login")
        except Exception:
            messages.error(request, "Something went wrong")
            return redirect("customer_register")
    return render(request, "customer/customer_register.html")



@login_required
def customerprofile(request):
    user=request.user
    if user.role !="CUSTOMER":
        return redirect("login")
    return render(request,'customer/profile.html',{"user":user})

def productlist(request):
    product=Product.objects.filter(approval_status="APPROVED").prefetch_related("images")
    return render(request,"customer/productlist.html",{"products":product})

def productcollection(request):
    return render(request,"customer/productcollection.html")

def productcategory(request):
    return render(request,"customer/productcategory.html")


def singleproduct(request,id):
    product=Product.objects.get(id=id)
    return render(request,"customer/singleproduct.html",{"product":product})
@login_required
def addcart(request,id):
    user=request.user
    product=Product.objects.get(id=id)
    cart,created=Cart.objects.get_or_create(user=user)
    
    try:
       cartitem=CartItem.objects.get(cart=cart,product=product)
       cartitem.quantity+=1
       cartitem.save()
    except:
        cartitem=CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=1,
            price_at_time=product.selling_price
        )
    return redirect("cartview")
@login_required
def cartview(request):
    user=request.user
    cartitem=CartItem.objects.filter(cart__user=user)
    return render(request,"customer/cart.html",{"cartitems":cartitem})

@login_required
def wishlist(request,id):
    user=request.user
    product=Product.objects.get(id=id)
    wishlist,created=Wishlist.objects.get_or_create(user=user)
    wishlistitem= WishlistItem.objects.filter(
        wishlist=wishlist,
        product=product
        ).first()
    if not wishlistitem:
        WishlistItem.objects.create(
            wishlist=wishlist,
            product=product
        )

    return redirect("wishlistview")
@login_required   
def wishlistview(request):
    user=request.user
    wishlistitem=WishlistItem.objects.filter(wishlist__user=user).distinct()
    return render(request,"customer/wishlist.html",{"wishlistitems":wishlistitem})

@login_required
def removewishlist(request,id):
    user=request.user
    WishlistItem.objects.filter(
        id=id,
        wishlist__user=user).delete()
    return redirect("wishlistview")


    








    


@login_required
def customer_dashboard(request):
    return render(request,"customer/dashboard.html")

#-----------------------------------------------------------------------
@login_required
def customerorder(request):
    return render(request,"customer/order.html")

@login_required
def customerwishlist(request):
    return render(request,"customer/wishlist.html")

@login_required
def customersettings(request):
    return render(request,"customer/settings.html")
