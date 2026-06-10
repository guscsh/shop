from .models import Category

def navbar_categories(request):
    # 只撈出啟用的主分類
    categories = Category.objects.filter(is_active=True, parent=None)
    return {'nav_categories': categories}
    # 改名為 nav_categories避免跟 product_list View 裡的 categories 衝突