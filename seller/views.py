from django.shortcuts import render,redirect
from core.models import User
from django.contrib.auth.decorators import login_required



def seller_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")



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
            last_name=last_name
        )
        user.save()
        return redirect("login")

    return render(request, "seller/register.html")


@login_required
def seller_dashboard(request):
   return render(request,"seller/seller_dashboard.html")
