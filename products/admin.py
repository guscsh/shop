from django.contrib import admin
from .models import Category, Product, Color, ProductImage, ProductVariant

# ------------------------------------------------------------------
# 1. Inlines (內嵌管理器) - 技術亮點：實現一站式編輯
# ------------------------------------------------------------------

class ProductImageInline(admin.TabularInline):
    """商品圖片內嵌：在商品頁直接上傳圖片並指定顏色"""
    model = ProductImage
    extra = 1
    max_num = 4 # 服裝通常 4-8 張圖即可
    ordering = ['display_order']
    # 限制可編輯欄位，讓介面更乾淨
    fields = ('image', 'color', 'alt_text', 'display_order')

class ProductVariantInline(admin.TabularInline):
    """商品頁直接管理 SKU (顏色+尺寸+庫存)"""
    model = ProductVariant
    extra = 1
    max_num = 20 
    ordering = ['color', 'size']
    readonly_fields = ('sku',) 

@admin.register(Color)
class Color(admin.ModelAdmin):
    list_display = ('name', 'slug', 'hex_code')
    search_fields = ('name','hex_code',)
    prepopulated_fields = {'slug': ('name',)}

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
# 3. Product Admin 
# ------------------------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'is_active', 'created_at', 'updated_at', )
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

    inlines = [ProductVariantInline, ProductImageInline]
