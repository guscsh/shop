from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('profile/', views.user_profile, name='profile'),
    # # 願望清單新增/移除 API (簡單版)
    # path('favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
]