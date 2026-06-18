from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# from django.core.mail import send_mail
from django.conf import settings
from carts.cart import Cart
from .forms import CheckoutForm
from .models import Order
from . import services


@login_required
def checkout(request):
    cart = Cart(request)

    # 購物車為空 → 擋下，導回購物車頁
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('carts:list')

    # unbound form（is_bound=False），會觸發 __init__ 內的 profile 預填邏輯
    form = CheckoutForm(user=request.user)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'cart_total': cart.get_total_price(),
    })


@login_required
def place_order(request):
    # 非 POST 請求（例如直接 GET 這個 URL）→ 導回 checkout 頁
    if request.method != 'POST':
        return redirect('orders:checkout')

    cart = Cart(request)

    # 雙重保險：即使繞過 checkout 直接 POST，空車也不允許下單
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('carts:list')

    # bound form（is_bound=True），不會觸發預填，保留使用者輸入
    form = CheckoutForm(request.POST, user=request.user)

    # 驗證失敗 → 重顯示結帳頁，form 會帶錯誤訊息與使用者剛剛的輸入
    if not form.is_valid():
        return render(request, 'orders/checkout.html', {
            'form': form,
            'cart': cart,
            'cart_total': cart.get_total_price(),
        })

    # 從 cleaned_data 組裝收件資訊（將由 service 複製成 Order 快照）
    shipping_data = {
        'full_name': form.cleaned_data['full_name'],
        'email': form.cleaned_data['email'],
        'phone': form.cleaned_data['phone'],
        'address': form.cleaned_data['address'],
    }

    # 取得脫敏後的付款資料（只剩末四碼，完整卡號不會離開 form）
    payment_data = form.get_payment_data()

    try:
        # 核心下單邏輯交給 service 處理（含 transaction.atomic 保護）
        order = services.place_order(request.user, cart, shipping_data, payment_data)
    except services.InsufficientStockError as e:
        # 庫存不足：把原因與缺貨明細存進 session，供 failed 頁顯示
        request.session['order_failed_reason'] = 'stock'
        request.session['order_failed_items'] = e.items
        return redirect('orders:failed')
    except ValueError:
        # 購物車空（service 內再檢查一次）→ 導回 cart 頁
        return redirect('carts:list')

    # 下單成功：寄確認信、清空購物車、導向成功頁
    cart.clear()
    return redirect('orders:success', order_no=order.order_no)

# def send_order_confirmation_email(order):
#     subject = f'Order Confirmation - {order.order_no}'

#     # 組裝信件本文（純文字）
#     lines = [
#         f'Hi {order.full_name},',
#         '',
#         f'Thank you for your order {order.order_no}.',
#         f'Total: ${order.total}',
#         '',
#         'Items:',
#     ]

#     # 逐筆列出訂單明細（items 是 OrderItem 的反向關聯）
#     for item in order.items.all():
#         lines.append(
#             f'- {item.product_name} ({item.color_name}/{item.size}) '
#             f'x{item.quantity} = ${item.subtotal}'
#         )

#     # 收件資訊
#     lines += [
#         '',
#         f'Shipping to: {order.address}',
#         f'Phone: {order.phone}',
#     ]

#     # 附加 Payment 資訊（OneToOne 反向關聯，不存在時 hasattr 為 False）
#     if hasattr(order, 'payment'):
#         payment = order.payment
#         lines += [
#             '',
#             f'Payment method: {payment.get_method_display()}',  # 取得 choice 的顯示名稱
#             f'Transaction ID: {payment.transaction_id}',
#             f'Card: **** **** **** {payment.card_last_four}',   # 只顯示末四碼
#         ]

#     send_mail(
#         subject=subject,
#         message='\n'.join(lines),
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[order.email],
#         fail_silently=False,  # 寄信失敗要拋例外，避免靜默漏信
#     )

@login_required
def order_success(request, order_no):
    # user=request.user 是防越權的關鍵條件
    order = get_object_or_404(
        Order.objects.select_related('payment'),  # 預先 JOIN，避免 N+1 查詢
        order_no=order_no,
        user=request.user,
    )
    return render(request, 'orders/success.html', {'order': order})


@login_required
def order_failed(request):
    # pop：取出並刪除，避免重新整理時還看到舊訊息
    reason = request.session.pop('order_failed_reason', None)
    items = request.session.pop('order_failed_items', [])

    return render(request, 'orders/failed.html', {
        'reason': reason,
        'failed_items': items,
    })