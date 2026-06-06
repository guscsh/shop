from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("shop_list")
    else:
        form = RegisterForm()
    return render(request,"accounts/register.html",{"form":form})

def logout_view(request):
    logout(request)
    return redirect("shop_list")