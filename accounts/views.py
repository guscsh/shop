from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("pages:shop_list")
    else:
        form = RegisterForm()
    return render(request,"accounts/register.html",{"form":form})

def logout_view(request):
    logout(request)
    next = request.GET.get('next')             # 取得要跳轉的網址
    is_safe = url_has_allowed_host_and_scheme( # 呼叫檢查工具
        url=request.GET.get('next'),           # 需檢查的網址字串
        allowed_hosts={request.get_host()},    # 允許的網域（通常是自己網站）
        require_https=request.is_secure()      # 如果目前係 https，就規定跳轉目標也必須是 https
    )
    if is_safe:                                # 如果安全
        return redirect(next)
    else:
        return redirect('pages:index')         # 如不安全，返回安全首頁

def profile(request):
    return render(request,"accounts/profile.html")