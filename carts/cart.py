from products.models import ProductVariant

class Cart:
    """購物車類別：基於 Session 運作"""
    
    def __init__(self, request):
        self.session = request.session
        carts = self.session.get('carts')
        if not carts:
            carts = self.session['carts'] = {}
        self.carts = carts

    def add(self, variant, quantity=1, override_quantity=False):
        variant_id = str(variant.id)
        if variant_id not in self.carts:
            self.carts[variant_id] = {
                'quantity': 0,
            }
        
        if override_quantity:
            self.carts[variant_id]['quantity'] = quantity
        else:
            self.carts[variant_id]['quantity'] += quantity
            
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, variant):
        variant_id = str(variant.id)
        if variant_id in self.carts:
            del self.carts[variant_id]
            self.save()

    def __iter__(self):
        variant_ids = self.carts.keys()
        
        # 預載入 product, color 和 product__images，避免 N+1 查詢
        variants = ProductVariant.objects.filter(
            id__in=variant_ids
        ).select_related('product', 'color').prefetch_related('product__images')
        
        cart = self.carts.copy()
        for variant in variants:
            cart[str(variant.id)]['variant'] = variant
            
        for item in cart.values():
            variant = item.get('variant')
            
            # 如果 variant 不存在(商品被刪)，跳過這筆資料，避免報錯
            if not variant:
                continue

            price = float(variant.final_price) 
            item['price'] = price
            item['total_price'] = item['price'] * item['quantity']
        
            # --- 尋找對應顏色的圖片 ---
            color_image = None
            color_image_text = None
            if variant.color:
                for img in variant.product.images.all():
                    if variant.color_id == img.color_id:
                        color_image = img.image
                        color_image_text = img.alt_text
                        break
                
                #找不到顏色圖，用封面圖
                if not color_image and variant.product.image:
                    color_image = variant.product.image
                    color_image_text = variant.product.name

            item['image'] = color_image
            item['image_text'] = color_image_text
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.carts.values())

    def get_total_price(self):
        variant_ids = self.carts.keys()      
        variants = ProductVariant.objects.filter(id__in=variant_ids).select_related('product')
        
        total = 0
        for variant in variants:
            qty = self.carts.get(str(variant.id), {}).get('quantity', 0)
            total += float(variant.final_price) * qty 
            
        return total

    def clear(self):
        del self.session['carts']
        self.save()