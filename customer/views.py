# from django.shortcuts import render,redirect
# from django.contrib import messages
# from core.models import *
# from seller.models import *
# from django.contrib.auth import authenticate,login
# from django.contrib.auth import get_user_model
# User = get_user_model()


# # Create your views here.
# def home_view(request):
#     return render(request,'core/home.html')
# def customer_register_view(request):
#     if request.method=="POST":
#         first_name=request.POST.get("first_name")
#         last_name=request.POST.get("last_name")
#         email=request.POST.get("email")
#         if email:
#             email = email.strip().lower()
#         password=request.POST.get("password")
#         confirm_password=request.POST.get("confirm_password")
#         print(first_name, email)
#         if password != confirm_password:
#             messages.error(request,'password do not match')
#             return redirect('/')
#         if User.objects.filter(email=email).exists():
#             messages.error(request,'email already exists')
#             return redirect('/')
#         user = User.objects.create_user( username=email, email=email, password=password, first_name=first_name, last_name=last_name )
#         return redirect('login')
#     return render(request,'core/customer_registartion.html')