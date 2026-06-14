# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from .models import UserProfile
# from products.models import Product

# @login_required # 亮點：保護 View，未登入自動跳轉登入頁
# def user_profile(request):
#     """
#     會員中心：顯示 VIP、積分、地址、歷史訂單、願望清單
#     """
#     # 技術亮點：用 get_or_create 防呆，避免因為沒建 Profile 而報錯
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
    
#     # 透過 related_name='orders' 撈歷史訂單 (假設 Order Model 已建立)
#     # orders = request.user.orders.all().order_by('-created_at')
    
#     context = {
#         'profile': profile,
#         # 'orders': orders,
#     }
#     return render(request, 'users/profile.html', context)


