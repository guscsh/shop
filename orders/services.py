import uuid                          
from decimal import Decimal          
from django.db import transaction    
from django.utils import timezone   
from products.models import ProductVariant  
from users.models import UserProfile 
from .models import Order, OrderItem, Payment  



class InsufficientStockError(Exception):
    def __init__(self, message, items=None):
        super().__init__(message)  # 呼叫父類 Exception 的 __init__，設定錯誤訊息
        # 避免直接傳入 None 在for時出錯,在None時傳入空列表
        self.items = items or []


def generate_order_no():
    return f"ORD-{timezone.now().strftime('%Y%m%d')}-{str(uuid.uuid4().int)[-12:]}"


@transaction.atomic  # 確保全成功
def place_order(user, cart, shipping_data, payment_data):
    cart_items = list(cart)
    if not cart_items:
        # 購物車空卻按結帳 → 直接擋下，不讓流程往下走
        raise ValueError('Cart is empty')

    # 收集購物車裡所有 variant 的 id
    variant_ids = [item['variant'].id for item in cart_items]

    # 一次撈出所有 variant，並做成 {id: variant} 的字典方便查表
    variants = {
        v.id: v
        for v in ProductVariant.objects.select_related('product', 'color')  
            .select_for_update()  # 這些列「上鎖」，其他表會自動鎖要修改必須等 commit
            .filter(id__in=variant_ids)
    }

    insufficient = []  # 收集所有缺貨的項目
    for item in cart_items:
        variant = variants.get(item['variant'].id)
        if not variant or variant.stock < item['quantity']:
            insufficient.append({
                'product': item['variant'].product.name,    
                'requested': item['quantity'],             
                'available': variant.stock if variant else 0,  
            })

    # 若有任何缺貨項目，一次拋出例外，帶上完整缺貨清單
    if insufficient:
        raise InsufficientStockError('Insufficient stock', insufficient)

    total = Decimal('0.00')
    order = Order.objects.create(
        user=user,
        order_no=generate_order_no(),
        # 下面四個是「收件快照」：從 shipping_data 複製一份進來
        # 未來使用者改 profile 不會影響這張訂單的收件資料
        full_name=shipping_data['full_name'],
        email=shipping_data['email'],
        phone=shipping_data['phone'],
        address=shipping_data['address'],
        total=Decimal('0.00'),   
        status='pending',         
    )

    for item in cart_items:
        variant = variants[item['variant'].id]   
        price = Decimal(str(item['price']))       
        qty = item['quantity']                    
        subtotal = price * qty                    
        total += subtotal                         

        # 只存 media 路徑字串（如 'products/tshirt_red.jpg'），不複製實體檔案
        # 若商品未來換圖，歷史訂單仍會顯示結帳當時的圖片路徑
        image_path = ''
        image_alt = ''
        if item.get('image'):
            image_path = item['image'].name           # .name 取得相對路徑
            image_alt = item.get('image_text', '')    

        # 從 variant 當下的值複製一份過來，未來商品改名不影響歷史訂單顯示
        OrderItem.objects.create(
            order=order,                          
            variant=variant,                      
            product_name=variant.product.name,    
            product_slug=variant.product.slug,    
            sku=variant.sku,                      
            color_name=variant.color.name,        
            size=variant.size,                    
            image_path=image_path,                
            image_alt=image_alt,                  
            price=price,                          
            quantity=qty,                         
            subtotal=subtotal,                    
        )

        # ---- 扣減庫存 ----
        variant.stock -= qty
        # update_fields=['stock']：只更新 stock 欄位
        variant.save(update_fields=['stock'])

    # 這是安全設計的核心 —— 敏感資料在 forms.get_payment_data() 階段就已被丟棄
    Payment.objects.create(
        order=order,                                              
        method=payment_data.get('method', 'credit_card'),         
        status='success',                                         
        amount=total,                                             
        card_last_four=payment_data.get('card_last_four', ''),    
        transaction_id=f"TXN-{uuid.uuid4().hex[:10].upper()}",    
        paid_at=timezone.now(),                                   
    )
    profile, _ = UserProfile.objects.get_or_create(user=user)

    earned_points = int(total)
    profile.points += earned_points
    profile.save(update_fields=['points'])
    order.total = total          
    order.status = 'paid'        
    order.save(update_fields=['status', 'total'])  
    return order                 