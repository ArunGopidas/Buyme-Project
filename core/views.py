from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
def login_view(request):
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        if not email or not password:
            return render(request,"login.html",{"error":"all fields are required"})
        
        email=email.strip().lower()

        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect("seller_dashboard")
        
        return render(request,"login.html",{"error":"invalid email or password"})
    return render(request,"login.html")

def seller_dashboard(request):
    return render(request, "seller/dashboard.html")

def customer_dashboard(request):
    return render(request, "customer/dashboard.html")

def admin_dashboard(request):
    return render(request, "customadmin/dashboard.html")