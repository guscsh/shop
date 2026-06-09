from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# ------------------------------------------------------------------
# 1. 商品列表頁
# ------------------------------------------------------------------
def product_list(request, category_slug=None):
    """
    商品列表頁：支援首頁全覽與分類篩選
    技術亮點：使用 Product.active.all() 而不是 Product.objects.all()
    """
    category = None
    categories = Category.objects.filter(is_active=True, parent=None) # 只取啟用的主分類
    
    # 亮點：這裡使用自定義 Manager，自動過濾下架商品且預載入圖片/變體
    products = Product.active.all() 

    # 如果有傳入 category_slug，代表使用者點擊了側邊欄的分類
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        # 亮點：如果是服裝，通常需要連同「子分類」的商品一起撈出來
        # 例如點擊「男裝」，應該要包含「男裝 > 上衣」和「男裝 > 褲子」的商品
        products = products.filter(category__in=category.get_descendants(include_self=True))

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'products/product_list.html', context)


# ------------------------------------------------------------------
# 2. 商品詳細頁
# ------------------------------------------------------------------
def product_pages(request, slug):
    """
    商品詳細頁：顯示單一商品資訊、顏色、尺寸、圖片
    技術亮點：同樣使用 active manager，確保下架商品無法被直接輸入網址觀看
    """
    # 亮點：使用 Product.active，如果該商品 is_active=False，會直接返回 404
    product = get_object_or_404(Product.active, slug=slug)
    
    # 由於我們在 ActiveProductManager 已經 prefetch_related('images', 'variants')
    # 這裡的 product.images.all() 和 product.variants.all() 不會再發出 SQL 查詢！
    
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)