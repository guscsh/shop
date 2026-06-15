from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from products.models import ProductVariant
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def carts_list(request):
    cart = Cart(request)
    return render(request, 'carts/carts_list.html', {'carts' : cart})

def carts_add(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant ,id=variant_id)
    quantity=int(request.GET.get('quantity', request.POST.get('quantity', 1)))
    cart.add(variant=variant, quantity=quantity)
    return redirect('carts:list')

def carts_remove(request, variant_id):
    cart = Cart(request)
    vartant = get_object_or_404(ProductVariant, id=variant_id)

    cart.remove(vartant)
    return redirect('carts:list')

def add_to_cart(request):
    # 1. 確保只有 POST 請求才能進來提交數據
    if request.method == 'POST':
        # 2. 透過 request.POST.get() 抓取前端 input 標籤中定義的 name 屬性
        sku = request.POST.get('sku')
        product_slug = request.POST.get('product_slug')
        quantity = int(request.POST.get('demo_vertical2', 1))

        # 2. 🛡️ 門神防禦：攔截空值或斷貨標籤
        if not sku or sku == 'out-of-stock':
            messages.error(request, "請先選擇有效的商品尺寸。")
            return redirect(request.META.get('HTTP_REFERER', 'products:list'))

        # 3. 🔄 橋樑對接：因為同學的 cart.add() 需要傳入「真實的 variant 物件」
        # 我們拿著前端傳來的唯一的 SKU，去資料庫精準打撈出這個物件
        variant = get_object_or_404(ProductVariant, sku=sku)

        # 4. 🛒 實例化同學寫的類別，交棒給它去處理 Session
        cart = Cart(request)
        
        # 💡 重點：直接呼叫同學的 add() 方法，把撈出來的 variant 和數量傳過去
        # 同學的底層會自己把 variant.id 轉成字串，並處理好內部的複數 'carts' Session
        cart.add(variant=variant, quantity=quantity)

        # 5. 🎉 成功反饋與最強重定向雙保險
        messages.success(request, f"成功將 {variant.product.name} ({variant.size}) 加入購物車！")
        return redirect(request.META.get('HTTP_REFERER', reverse('products:product', kwargs={'slug': product_slug})))

    # 如果有人用 GET 偷敲網址，直接踢回商品列表頁
    return redirect('products:list')