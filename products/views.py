from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product

def product_list(request):
    """商品列表頁：支援分類、價格篩選 + 分頁"""
    selected_category = request.GET.get('category', '')#取出 category 參數，如果沒有則預設為空字串。
    max_p = request.GET.get('max', '')
    
    categories = Category.objects.filter(is_active=True, parent=None)#取出頂層分類（沒有 parent 的主分類），且必須是上架狀態。

    # 計算主分類總數 (本身 + 子分類)
    for cat in categories: #來自 models.py 中 related_name='children' 的反向關聯。
        category_ids = [cat.id] + list(cat.children.values_list('id', flat=True)) #只取出 id 欄位，變成一個 list。
        cat.total_product_count = Product.active.filter(category_id__in=category_ids).count()
        
        # 核心修復：將子分別轉為 list 並計算數量，再掛回 cat 物件
        sub_cats = list(cat.children.all()) # 強制執行查詢並轉成 Python list，避免後續模板中重複查詢資料庫。
        for sub in sub_cats:
            sub.sub_product_count = Product.active.filter(category_id=sub.id).count()#為每個子分類計算商品數量，並新增 sub_product_count 屬性,
        cat.sub_categories = sub_cats#把處理好的子分類清單掛到 cat.sub_categories

    # === 3. 商品查詢 ===
    products = Product.active.all()
    
    # 分類篩選 (這裡也要包含子分類)
    if selected_category:
        category = get_object_or_404(Category, slug=selected_category)
        category_ids = [category.id] + list(category.children.values_list('id', flat=True))
        products = products.filter(category_id__in=category_ids)

    # 價格篩選
    if max_p:
        try:
            max_price = float(max_p)
            products = products.filter(base_price__lte=max_price)#小於等於（less than or equal）指定的最高價格。
        except ValueError:
            pass
    
    # === 4. 計算總數 (在分頁前) ===
    total_products = products.count()#在套用分頁前先計算總商品數，供模板顯示「共 X 件商品」。
    
    # === 5. 分頁 ===
    paginator = Paginator(products, 6) #每頁顯示 10 筆商品
    page_number = request.GET.get('page', 1)#取得當前頁面的資料
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'products': page_obj, 
        'total_products': total_products,
        'selected_category': selected_category,
        'max_p': max_p,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'products/product_list.html', context)

# ------------------------------------------------------------------
# 2. 商品詳細頁
# ------------------------------------------------------------------
def product(request, slug):
    """
    商品詳細頁：顯示單一商品資訊、顏色、尺寸、圖片
    技術亮點：同樣使用 active manager，確保下架商品無法被直接輸入網址觀看
    """
    product = get_object_or_404(Product.active, slug=slug)#如果商品已下架（is_active=False），即使知道網址也會看到 404，防止已下架商品被直接訪問
    
    # 由於我們在 ActiveProductManager 已經 prefetch_related('images', 'variants')
    # 這裡的 product.images.all() 和 product.variants.all() 不會再發出 SQL 查詢！
    
    context = {
        'product': product,
    }
    return render(request, 'products/product.html', context)