from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import *
from seller.models import *
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        user=request.user
        return render(request,'customer/home.html',{'user':user})
    return render(request,'customer/home.html')

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
def customer_dashboard(request):
    return render(request,"customer/dashboard.html")