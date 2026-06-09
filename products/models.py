from django.db import models 
from django.urls import reverse # 用來動態反推 URL 路徑，避免把網址寫死
from django.utils.text import slugify # 將中英文標題轉換成 URL 友善的格式 (如：Hello World -> hello-world)


# 1. 分類
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)# 專門存 URL 路徑的欄位，只允許字母、數字、底線、連字號
    is_active = models.BooleanField(default=True, verbose_name='Is_Published')
    parent = models.ForeignKey(
        'self', # 關聯到自己！這是樹狀結構的關鍵，表示 parent 指向另一個 Category
        null=True, 
        blank=True, 
        on_delete=models.PROTECT, # 刪除保護機制！如果該分類底下還有子分類，不允許刪除，拋出 ProtectedError
        related_name='children')# 反向查詢名稱：可以透過 category.children.all() 撈出所有子分類

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        # 自動生成 Slug
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ActiveProductManager(models.Manager):
    """只取出上架商品，並預載入圖片和最低價格變體，避免 N+1 Query"""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).prefetch_related('images', 'variants')

# 2. 商品主檔
class Product(models.Model):
    category = models.ForeignKey(# 外鍵：商品屬於哪個分類
        Category, 
        on_delete=models.PROTECT, # 防呆：有商品的分類不允許被刪除
        related_name='products', 
        verbose_name='category'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)# 專門存 URL 路徑的欄位，只允許字母、數字、底線、連字號
    description = models.TextField(null=True)
    
    # 技術亮點：基礎價格保留作為篩選或列表顯示，實際結帳以 Variant 為準
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    is_active = models.BooleanField(default=True, db_index=True) # 加索引加速後台/列表查詢
    created_at = models.DateTimeField(auto_now_add=True)# 建立時間，只在資料「第一次新增」時自動填入當下時間
    updated_at = models.DateTimeField(auto_now=True)# 更新時間，每次「執行 save()」都會自動更新為當下時間

    # 技術亮點：自定義 Manager，預設只取出上架商品
    objects = models.Manager() # 保留 Django 預設 Manager，後台可以用它撈出所有商品(含下架)
    active = ActiveProductManager() # 定義在下方
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['created_at'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:pages', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

# 4. 顏色選項
class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    name = models.CharField(max_length=50, verbose_name='Color Name (e.g. Classic Black)')
    hex_code = models.CharField(max_length=7, verbose_name='HexCode (e.g.#000000)', help_text='Format: #RRGGBB')
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'name') # 同商品不能有重複顏色名
        ordering = ['display_order']
        indexes = [models.Index(fields=['display_order'])]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

# 3. 商品圖片 - 技術亮點：支援多圖與綁定顏色
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    alt_text = models.CharField(max_length=150, blank=True, verbose_name='SeoKeywords')#圖片替代文字 (SEO)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order'] # 依排序欄位排列
        indexes = [models.Index(fields=['display_order'])]

    def save(self, *args, **kwargs):
        # 如果營運人員沒有填寫 alt_text，就自動填入商品名稱
        if not self.alt_text and self.product:
            self.alt_text = self.product.name
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"




# 5. 商品規格 - 核心邏輯：顏色 + 尺寸 = 庫存與價格
class ProductVariant(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'), 
        ('L', 'L'), ('XL', 'XL'), ('2XL', '2XL'),('3XL','3XL')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(ProductColor, on_delete=models.PROTECT, related_name='variants')
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    stock = models.PositiveIntegerField(default=0, db_index=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)

    class Meta:
        # 核心邏輯：同一商品的同顏色同尺寸只能有一筆
        unique_together = ('product', 'color', 'size') 
    
    def save(self, *args, **kwargs):
        # 技術亮點：自動生成 SKU 邏輯
        if not self.sku:
            # 規則範例：商品Slug-顏色代號-尺寸 (例如: classic-t-shirt-BK-M)
            product_slug = self.product.slug[:20] # 避免過長，取前 20 字
            color_name = self.color.name[:2].upper() # 取顏色前兩字大寫，如 BLACK -> BL
            size = self.size
            
            base_sku = f"{product_slug}-{color_name}-{size}"
            
            # 確保唯一性：如果萬一發生碰撞，加上隨機碼或流水號
            # 這裡用簡單的 while 迴圈示範
            unique_sku = base_sku
            counter = 1
            while ProductVariant.objects.filter(sku=unique_sku).exists():
                unique_sku = f"{base_sku}-{counter}"
                counter += 1
            self.sku = unique_sku

        if self.price is None or self.price == 0:
            self.price = self.product.base_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.color.name} / {self.size}"


class ProductInventory(Product):
    """商品庫存與圖片管理的 Proxy Model"""
    class Meta:
        proxy = True  # 重點：這是一個代理模型，不建新表
        verbose_name = "ProductVariant"
        verbose_name_plural = "ProductVariant"

        