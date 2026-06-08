from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'MemberInfo'
    
    # 將願望清單改為雙欄篩選器！
    filter_horizontal = ('favorites',)
    
    # 1. 設定可編輯欄位（確保只有 points 和地址等可以改）
    fields = ('phone', 'address', 'points', 'vip_level_display', 'favorites')
    
    # 2. 設定唯讀欄位（因為 vip_level_display 是動態算的，必須設為唯讀才能顯示在編輯頁）
    readonly_fields = ('vip_level_display',)

    # 3. 在編輯頁顯示中文 VIP 等級的方法
    def vip_level_display(self, obj):
        return obj.vip_level_display #呼叫 Model 裡的 @property 取得計算後的等級。
    vip_level_display.short_description = 'Current VIP Level' #設定這個欄位在後台顯示的標籤名稱。

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    
    # 4. 在列表頁也顯示 VIP 等級和積分
    list_display = ('username', 'email', 'get_vip_level', 'get_points', 'is_staff')
    
    def get_vip_level(self, obj):
        return obj.profile.vip_level_display
    get_vip_level.short_description = 'VIP Level'

    def get_points(self, obj):
        return obj.profile.points
    get_points.short_description = 'Points'

# 重新註冊 User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)