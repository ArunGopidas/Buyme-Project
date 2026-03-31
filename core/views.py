from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from seller.models import SellerProfile


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
            if user.role =="SELLER":
                try:
                    seller = SellerProfile.objects.get(user=user)

                    if seller.status =="PENDING":
                        return redirect('pending_approval')

                    elif seller.status == "APPROVED":
                        return redirect("seller_dashboard")

                    elif seller.status == "REJECTED":
                        return redirect("rejected_page")

                except SellerProfile.DoesNotExist:
                    return redirect('seller_profile')

            elif user.role =="CUSTOMER":
                return redirect('home')

            elif user.role =="ADMIN":
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        return render(request,"core/login.html",{"error":"invalid email or password"})
    return render(request,"core/login.html")

def logout_view(request):
    logout(request)
    return redirect("/")
