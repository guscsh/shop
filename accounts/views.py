from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash #改密碼後更新 session，避免被登出
from django.contrib.auth.decorators import login_required #登入驗證裝飾器，確保只有登入的使用者才能訪問特定視圖
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin #類別型視圖的登入驗證，確保只有登入的使用者才能訪問特定視圖
from .forms import RegisterForm, ProfileUpdateForm, CustomPasswordForm #表單類別，用於註冊、更新使用者資料和密碼
from users.models import UserProfile #使用者模型，包含使用者資料和關聯的訂單、願望清單等
from products.models import Product #商品模型，包含商品資料和關聯的使用者、商品等
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
# from orders.models import Order #訂單模型，包含訂單資料和關聯的使用者、商品等
from PIL import Image #圖片處理庫，用於圖片裁剪和縮放
# from django.utils.http import url_has_allowed_host_and_scheme #URL 驗證工具，確保重定向的 URL 安全
# from django.contrib.auth.views import LoginView #登入視圖，用於處理登入流程

# class CustomLoginView(LoginView):
#     template_name = "accounts/login.html"
#     redirect_authenticated_user = True

def register_view(request):
    if request.method == "POST": #如果請求方法是 POST，則處理表單提交
        form = RegisterForm(request.POST)#表單驗證，request.POST 包含使用者提交的表單資料
        if form.is_valid(): #表單驗證成功，則保存使用者資料並登入
            user = form.save()#保存使用者資料並返回 User 物件
            login(request, user)#登入使用者
            return redirect("pages:index")
    else: #如果請求方法是 GET，則顯示註冊表單       
        form = RegisterForm() #創建一個新的 RegisterForm 物件
    return render(request, "accounts/register.html", {"form": form}) #渲染註冊頁面，並傳遞表單物件


# # Logout
# def logout_view(request):
#     logout(request)
#     next_url = request.GET.get('next')#獲取重定向的 URL
#     is_safe = url_has_allowed_host_and_scheme(#驗證 URL 是否安全，避免重定向到惡意網站
#         url=next_url, #要驗證的 URL
#         allowed_hosts={request.get_host()}, #允許的主機列表
#         require_https=request.is_secure() #是否要求 HTTPS
#     )
#     if is_safe and next_url: #如果 URL 安全且存在，則重定向到該 URL
#         return redirect(next_url) #重定向到該 URL
#     return redirect('pages:index') #如果 URL 不安全或不存在，則重定向到首頁


# # Get or create user profile
# def get_or_create_profile(user):
#     profile, created = UserProfile.objects.get_or_create(user=user)
#     return profile


# Profile page
@login_required#登入驗證裝飾器，確保只有登入的使用者才能訪問特定視圖
def profile(request):
    user = request.user #獲取當前登入的使用者
    # if not user.is_authenticated:
    #     return redirect('accounts:login')
    profile, _ = UserProfile.objects.get_or_create(user=user)#獲取或創建使用者資料

    profile_form = ProfileUpdateForm(instance=profile, user=user)#表單填入現有資料
    pwd_form = CustomPasswordForm(user)#創建改密碼表單 

    if request.method == "POST":#如果請求方法是 POST，則處理表單提交            
        profile_form = ProfileUpdateForm(#創建一個新的 ProfileUpdateForm 物件，包含使用者提交的表單資料
            request.POST, request.FILES, instance=profile, user=user# 文字 + 上傳頭像資料
        )
        pwd_form = CustomPasswordForm(user, request.POST)#表單填入現有資料 + 新密碼
        password_attempted = bool(request.POST.get('new_password1'))#如果新密碼被提交，則設置為 True，否則設置為 False
        profile_ok = profile_form.is_valid()#如果表單驗證成功，則設置為 True，否則設置為 False
        password_ok = pwd_form.is_valid() if password_attempted else True#如果新密碼被提交，則驗證新密碼，否則設置為 True
        
        if profile_ok and password_ok:#如果表單驗證成功，則更新使用者資料
            # 儲存 profile + 必要時改密碼
            user.first_name = profile_form.cleaned_data['first_name']#更新使用者名稱
            user.last_name = profile_form.cleaned_data['last_name']#更新使用者姓氏
            user.save()

            profile = profile_form.save(commit=False)#保存使用者資料
            profile.user = user#設置使用者資料

            # Avatar crop & resize
            if profile.avatar:#如果使用者有頭像，則保存頭像     
                profile.save()#保存使用者資料
                img_path = profile.avatar.path#獲取頭像路徑
                try:
                    img = Image.open(img_path).convert("RGB")#打開頭像
                    x = int(profile.crop_x)#獲取裁剪位置
                    y = int(profile.crop_y)#獲取裁剪位置
                    w = int(profile.crop_w)#獲取裁剪寬度
                    h = int(profile.crop_h)#獲取裁剪高度

                    if w > 0 and h > 0:#如果裁剪寬度和大於 0，則裁剪頭像
                        img = img.crop((x, y, x + w, y + h))#裁剪頭像
                    img = img.resize((300, 300), Image.Resampling.LANCZOS)#調整頭像大小
                    img.save(img_path, "JPEG", quality=85)#保存頭像
                except Exception:#如果頭像處理失敗，則跳過
                    pass
            else:
                profile.save()#保存使用者資料

            # Change password
            # if request.POST.get('new_password1'):#如果請求方法是 POST，則處理表單提交
            #     if pwd_form.is_valid():#如果表單驗證成功，則保存使用者資料
            #         pwd_form.save()#保存使用者資料
            #         update_session_auth_hash(request, user)#更新 session，避免被登出
            if password_attempted:
                pwd_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Profile and password updated successfully.')
            else:
                messages.success(request, 'Profile updated successfully.')
            
            return redirect('accounts:profile')#重定向到使用者資料頁面
        else:
            messages.error(request, 'Please correct the errors below.')#如果表單驗證失敗，則顯示錯誤訊息

    context = {
        'profile_form': profile_form, 
        'pwd_form': pwd_form, 
        'user': user, 
        'profile': profile 
    }
    return render(request, "accounts/profile.html", context)    


# Dashboard
class AccountDashboard(LoginRequiredMixin, TemplateView):#未登入自動跳登入頁面
    template_name = "accounts/dashboard.html"#顯示儀表板頁面

    def get_context_data(self, **kwargs):#準備 template 變數
        context = super().get_context_data(**kwargs)#獲取上下文物件
        user = self.request.user#獲取當前登入的使用者
        context["user"] = user#傳遞使用者物件

        # Auto create profile if missing (fix User has no profile error)
        profile, _ = UserProfile.objects.get_or_create(user=user)#獲取或創建使用者資料

        context["point_balance"] = profile.points#傳遞積分
        # context["vip_level"] = profile.vip_level_display#傳遞 VIP 等級
        # fix order
        # context["order_history"] = Order.objects.filter(user=user).count()
        context["order_history"] = 0#傳遞訂單數量
        context["total_favourites"] = profile.favorites.count()#傳遞願望清單數量
        return context#返回上下文物件


# Order History
@login_required
def order_history(request):
    # fix order
    # orders = Order.objects.filter(user=request.user).order_by('-date')
    orders = []
    return render(request, "accounts/orders.html", {#傳遞訂單列表和使用者物件
        "order_list": orders, #訂單列表
        "user": request.user #使用者物件
    })#渲染訂單頁面，並傳遞上下文物件


# Favourites (use UserProfile M2M field)
@login_required
def favourites(request):#顯示願望清單頁面
    profile, _ = UserProfile.objects.get_or_create(user=request.user)#獲取或創建使用者資料
    fav_list = profile.favorites.all() #拿取UserProfile模型中的favorites關聯的Product物件
    return render(request, "accounts/favourites.html", {#傳遞願望清單列表和使用者物件
        "fav_list": fav_list, #願望清單列表
        "user": request.user #使用者物件
    })#渲染願望清單頁面，並傳遞上下文物件

@login_required
def toggle_favourite(request, product_id):
    """
    願望清單切換：有就移除，沒有就加入
    """
    profile = request.user.profile#獲取使用者資料
    product = get_object_or_404(Product, id=product_id)#獲取商品資料
    
    if product in profile.favorites.all():
        # 如果已在清單中 -> 移除
        profile.favorites.remove(product)
        status = 'removed'
    else:
        # 如果不在清單中 -> 加入
        profile.favorites.add(product)
        status = 'added'
    
    # 支援一般表單提交與 AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'product_id': product_id})# 
    else:
        return redirect(request.META.get('HTTP_REFERER', 'products:list'))