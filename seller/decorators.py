from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



def seller_required(view_function):
    @login_required
    def wrapper(request,*args,**kwargs):
        if request.user.role != "SELLER":
            return redirect("login")

        seller=request.user.seller_profile

        if seller.status == "PENDING":
            return redirect('pending_approval')

        if seller.status == "REJECTED":
            return redirect("rejected_page")

        return view_function(*args,**kwargs)

    return wrapper