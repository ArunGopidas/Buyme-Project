from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps



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