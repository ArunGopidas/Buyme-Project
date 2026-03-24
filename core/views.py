from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
def login_view(request):
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        if not email or not password:
            return render(request,"core/login.html",{"error":"all fields are required"})

        email=email.strip().lower()

        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request, user)
            if user.role=="SELLER":
                return redirect("seller_dashboard")
            elif user.role =="ADMIN":
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        return render(request,"login.html",{"error":"invalid email or password"})
    return render(request,"core/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")
