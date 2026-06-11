from django.urls import path
from . import views

app_name = 'products' # 對應 models.py 裡面的 reverse('products:product')

# 這個變數名稱絕對不能拼錯！
urlpatterns = [
    path('', views.product_list, name='list'),
    path('<slug:slug>/', views.product, name='product'),
]