from django.conf import settings
from django.db import models


class Order(models.Model):
    """
    訂單主檔：一位使用者可有多筆訂單，每筆訂單包含收件資訊、總金額與狀態。
    收件人欄位為「快照」，保存下單當下的資料，避免使用者日後改 profile 後訂單紀錄對不上。
    付款細節由關聯的 Payment 模型記錄（一對一）。
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),      # 待付款（建立訂單時的初始狀態）
        ('paid', 'Paid'),            # 已付款（Payment 建立成功後更新）
        ('failed', 'Failed'),        # 付款失敗
        ('cancelled', 'Cancelled'),  # 已取消（Admin 手動取消）
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,   # 有訂單的 user 不能被硬刪
        related_name='orders'       # user.orders 可反向查詢該使用者的所有訂單
    )
    order_no = models.CharField(max_length=50, unique=True)  # 訂單編號，全系統唯一

    # 收件人快照（checkout 當下從表單複製進來，不隨 profile 變動）
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    total = models.DecimalField(max_digits=10, decimal_places=2)  # 所有 OrderItem subtotal 加總
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間，只寫入一次
    updated_at = models.DateTimeField(auto_now=True)      # 每次儲存時自動更新

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_no']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.order_no


class OrderItem(models.Model):
    """
    訂單明細：一筆訂單可有多個商品項目（一對多）。
    除了關聯 variant 外，也保存商品名稱、價格、圖片等快照，
    即使商品日後改名、改價或下架，歷史訂單仍顯示下單當下的內容。
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,  # 訂單刪除時，明細一併刪除
        related_name='items'       # order.items 可取得該訂單所有品項
    )

    # 保留 FK 供後台追蹤來源；前台顯示應以下方快照欄位為準
    variant = models.ForeignKey(
        'products.ProductVariant',
        on_delete=models.PROTECT,  # 已被訂單引用的規格不可刪除
        related_name='order_items'
    )

    # 商品快照（checkout 當下由 services 寫入）
    product_name = models.CharField(max_length=200)
    product_slug = models.SlugField(max_length=200, blank=True)
    sku = models.CharField(max_length=50, blank=True)
    color_name = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=5)

    # 圖片快照：只存 media 相對路徑，不複製實體檔案
    image_path = models.CharField(max_length=255, blank=True)
    image_alt = models.CharField(max_length=150, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)     # 下單時單價
    quantity = models.PositiveIntegerField()                         # 購買數量
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # 小計 = price × quantity

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    @property # 把這個function註冊為 Getter（讀取器）Template呼叫時不用加括號就可以直接使用
    def image_url(self):
        """組合 MEDIA_URL 與 image_path，供 template 顯示商品圖。"""
        if self.image_path:
            return f'{settings.MEDIA_URL}{self.image_path}'
        return ''

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'


class Payment(models.Model):
    """
    付款紀錄：與 Order 一對一關聯，記錄每筆訂單的付款方式與結果。
    只存卡號末四碼與模擬交易編號，不儲存完整信用卡號或 CVC（資安考量）。
    """

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'  # order.payment 可反向取得付款紀錄
    )
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='credit_card')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 實際付款金額（應等於 order.total）

    # 功課用模擬欄位 — 絕對不要存完整卡號 / CVC
    card_last_four = models.CharField(max_length=4, blank=True)    # 卡號末四碼，供確認信顯示
    transaction_id = models.CharField(max_length=100, blank=True)  # 模擬交易編號（如 TXN-XXXXXXXXXX）

    paid_at = models.DateTimeField(null=True, blank=True)  # 付款成功時間
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order.order_no} - {self.get_status_display()}'
