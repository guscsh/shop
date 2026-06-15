from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from products.models import ProductVariant
from django.contrib import messages

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
        variant_id = request.POST.get('variant_id')
        sku = request.POST.get('variant_sku')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')
        product_slug = request.POST.get('product_slug')

        # 3. 初始化或獲取當前 Session 裡面的購物車字典
        cart = request.session.get('cart', {})
        
        # 4. 堆疊數量邏輯（如果購物車已有該 SKU，數量累加；否則全新建立，預設 Quantity 為 0，然後再累加）
        cart.setdefault(sku, {'variant_id': variant_id, 'quantity': 0, 'size': size})['quantity'] += quantity
            
        # 5. 將更新後的數據重新寫回 Session 儲存
        request.session['cart'] = cart
        
        # 6. 利用 Django 訊息框架，在網頁刷新後跳出提示（可選）
        messages.success(request, f"Successfully added {quantity} item(s) to your cart!")
        
        # 7. 🎯 終極核心：重新定向回用家剛才瀏覽的商品頁（防止網頁重新整理時重複提交表單）
        if product_slug:
            return redirect('products:product', slug=product_slug)
                    
        # 如果沒有 product_slug，request.META.get('HTTP_REFERER') 會抓取用家點擊按鈕前的上一個網址
        return redirect(request.META.get('HTTP_REFERER', 'products:list'))
        
    # 如果有人用 GET 方式偷敲這個網址，直接踢回商品列表頁
    return redirect('products:list')