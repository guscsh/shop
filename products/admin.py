from django.contrib import admin
from .models import Category, Product, ProductColor, ProductImage, ProductVariant, ProductInventory

# ------------------------------------------------------------------
# 1. Inlines (內嵌管理器) - 技術亮點：實現一站式編輯
# ------------------------------------------------------------------

class ProductColorInline(admin.TabularInline):
    """商品顏色內嵌：在商品頁直接新增顏色與色碼"""
    model = ProductColor
    extra = 1 # 預設顯示幾排空白欄位供填寫
    max_num = 10 # 限制最多 10 個顏色，避免前端按鈕過多
    ordering = ['display_order'] # 根據我們在 Model 設定的排序


class ProductImageInline(admin.TabularInline):
    """商品圖片內嵌：在商品頁直接上傳圖片並指定顏色"""
    model = ProductImage
    extra = 1
    max_num = 4 # 服裝通常 4-8 張圖即可
    ordering = ['display_order']
    # 限制可編輯欄位，讓介面更乾淨
    fields = ('image', 'color', 'alt_text', 'display_order')

class ProductVariantInline(admin.TabularInline):
    """商品變體內嵌：在商品頁直接管理 SKU (顏色+尺寸+庫存)"""
    model = ProductVariant
    extra = 3 # 預設 3 排，通常一件衣服至少 S/M/L
    max_num = 20 
    ordering = ['color', 'size']
    # 技術亮點：readonly_fields。因為 SKU 通常有特定編碼規則，不讓人亂改
    readonly_fields = ('sku',) 
    # fields = ('sku',) 



# ------------------------------------------------------------------
# 2. Category Admin
# ------------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'product_count')
    list_filter = ('parent',)
    search_fields = ('name',)
    # 技術亮點：自動根據 name 填入 slug，後台人員不用自己想網址
    prepopulated_fields = {'slug': ('name',)}
    list_editable = 'is_active',
    
    # 自定義欄位：顯示該分類下有多少商品，方便店長評估分類熱度
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Quantity'


# ------------------------------------------------------------------
# 3. Product Admin - 核心大魔王
# ------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ('name', 'category', 'base_price', 'is_active', 'created_at', 'updated_at', )
    list_filter = ('category', 'created_at')
    list_editable = 'is_active',
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    # 技術亮點：將日期和狀態設為唯讀，避免人為誤改系統時間
    readonly_fields = ('created_at', 'updated_at')
    
    # 技術亮點：Fieldsets 分組，讓後台介面排班整齊，UX 極佳
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category')
        }),
        ('DetailContent', {
            'fields': ('description',)
        }),
        ('PriceStatus', {
            'fields': ('base_price', 'is_active', 'created_at', 'updated_at')
        }),
        ('Image',{
            'fields':('image',)
        }),
    )

    # 技術亮點：把 Inlines 掛載進來！這是這個架構的靈魂
    inlines = [ProductColorInline,]
    
    def inventory_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        # 找到 ProductInventory 的 change page 網址
        url = reverse('admin:products_productinventory_change', args=[obj.pk])
        return format_html('<a href="{}">ProductVariant</a>', url)
    inventory_link.short_description = 'ProductVariant'

    list_display = ('name', 'category', 'base_price','created_at', 'updated_at', 'inventory_link','is_active')

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    # 重點：這裡掛上 Inlines！
    inlines = [ProductVariantInline, ProductImageInline]
    
    # 優化 UX：因為這個頁面專門編輯庫存，商品名稱等基本資料設為唯讀即可，防止誤改
    readonly_fields = ('name', 'category', 'base_price', 'description')
    
    fieldsets = (
        ('Info', {
            'fields': ('name', 'category', 'base_price', 'description')
        }),
    )
    
    # 覆寫 queryset，確保權限和顯示邏輯與 Product 一致
    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_active=True)