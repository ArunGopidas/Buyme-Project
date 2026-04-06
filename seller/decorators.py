from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from functools import wraps
from .models import SellerProfile

def seller_required(view_function):
    @login_required
    @wraps(view_function)
    def wrapper(request,*args,**kwargs):
        if request.user.role != "SELLER":
            return redirect("login")
        try:
            seller=request.user.seller_profile
        except:
            return redirect("seller_profile")
        if seller.status == "PENDING":
            return redirect('pending_approval')

        if seller.status == "REJECTED":
            return redirect("rejected_page")

        return view_function(request,*args,**kwargs)

    return wrapper

def new_seller_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.role != "SELLER":
            return redirect("home")
        seller = SellerProfile.objects.filter(user=request.user).first()
        if seller:
            if seller.status == "PENDING":
                return redirect('pending_approval')
            elif seller.status == "REJECTED":
                return redirect("approval_rejection")
            else:
                return redirect("seller_dashboard")
        return view_func(request, *args, **kwargs)
    return wrapper