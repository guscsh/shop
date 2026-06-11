from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    # Avatar crop & resize
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    crop_x = models.CharField(max_length=10, default="0")
    crop_y = models.CharField(max_length=10, default="0")
    crop_w = models.CharField(max_length=10, default="0")
    crop_h = models.CharField(max_length=10, default="0")

    # --- 積分與 VIP 改動 ---
    points = models.PositiveIntegerField( #正整數欄位
        default=0, 
    )
    
    favorites = models.ManyToManyField(
        'products.Product', 
        blank=True, 
        related_name='favorited_by'
    )

    # 技術亮點：@property 將方法變成屬性，VIP 等級隨插即用！
    @property
    def vip_level(self):
        """根據積分自動計算 VIP 等級"""
        if self.points >= 10000:
            return 'diamond'
        elif self.points >= 5000:
            return 'gold'
        elif self.points >= 1000:
            return 'silver'
        else:
            return 'normal'

    @property
    def vip_level_display(self):
        """回傳 VIP 等級，方便 Admin 和 Template 使用"""
        VIP_MAP = {
            'normal': 'Regular Member',
            'silver': 'Silver Member',
            'gold': 'Gold Member',
            'diamond': 'Diamond Member',
        }
        return VIP_MAP.get(self.vip_level, 'Unknown Level')#如果 vip_level 邏輯出錯回傳了不存在的值，使用 .get() 可以避免程式直接拋出 KeyError 崩潰，而是會回傳後備的 'Unknown Level'

    def __str__(self):
        return f"{self.user.username} User Profile"
    
# Auto create & save profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()