from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProfile
from products.models import Product

@login_required # 亮點：保護 View，未登入自動跳轉登入頁
def user_profile(request):
    """
    會員中心：顯示 VIP、積分、地址、歷史訂單、願望清單
    """
    # 技術亮點：用 get_or_create 防呆，避免因為沒建 Profile 而報錯
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # 透過 related_name='orders' 撈歷史訂單 (假設 Order Model 已建立)
    # orders = request.user.orders.all().order_by('-created_at')
    
    context = {
        'profile': profile,
        # 'orders': orders,
    }
    return render(request, 'users/profile.html', context)


@login_required
def toggle_favorite(request, product_id):
    """
    願望清單切換：有就移除，沒有就加入
    技術亮點：ManyToManyField 的 add()/remove() 操作
    """
    profile = request.user.profile
    product = get_object_or_404(Product, id=product_id)
    
    if product in profile.favorites.all():
        # 如果已在清單中 -> 移除
        profile.favorites.remove(product)
        status = 'removed'
    else:
        # 如果不在清單中 -> 加入
        profile.favorites.add(product)
        status = 'added'
    
    # 實戰考量：支援一般表單提交與 AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # 如果前端用 AJAX 發送，回傳 JSON
        return JsonResponse({'status': status, 'product_id': product_id})
    else:
        # 如果是傳統表單，回到上一頁
        return redirect(request.META.get('HTTP_REFERER', 'products:list'))