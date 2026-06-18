from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    """訂單明細內嵌顯示，供 Admin 在同一頁管理品項。"""
    model = OrderItem
    extra = 0
    readonly_fields = (
        'product_name', 'sku', 'color_name', 'size',
        'price', 'quantity', 'subtotal', 'image_path',
    )


class PaymentInline(admin.StackedInline):
    """付款紀錄內嵌顯示，與 Order 一對一。"""
    model = Payment
    extra = 0
    readonly_fields = ('transaction_id', 'paid_at', 'created_at')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'user', 'product_summary', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_no', 'full_name', 'email', 'phone')
    readonly_fields = ('order_no', 'created_at', 'updated_at')
    inlines = [OrderItemInline, PaymentInline]
    fields = (
        'order_no', 'user', 'status',
        'full_name', 'email', 'phone', 'address',
        'total', 'created_at', 'updated_at',
    )

    @admin.display(description='Products')
    def product_summary(self, obj):
        # 用快照 product_name，不要用 variant.product.name（歷史訂單較準確）
        names = [item.product_name for item in obj.items.all()]
        return ', '.join(names) if names else '—'
    def get_queryset(self, request):
        # 避免列表每一筆訂單都多查一次 items（N+1）
        qs = super().get_queryset(request)
        return qs.prefetch_related('items')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'method', 'status', 'amount', 'card_last_four', 'paid_at')
    list_filter = ('status', 'method', 'paid_at')
    search_fields = ('transaction_id', 'order__order_no', 'card_last_four')
    readonly_fields = ('transaction_id', 'paid_at', 'created_at')
