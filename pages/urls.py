from django.urls import path
from . import views
from .views import subscribe_newsletter

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog/post/', views.blog_post, name='blog_post'),
    path('shop/', views.shop_list, name='shop_list'), 
    path('subscribe/', subscribe_newsletter, name='subscribe'),
    path('faqs/', views.faqs, name='faqs'),
    path('shipping_info/', views.shipping_info, name='shipping_info'),
    path('return_info/', views.return_info, name='return_info'),
    path('payment_info/', views.payment_info, name='payment_info'),
    path('test/', views.test, name='test'),
]

handler404 = 'pages.views.custom_404'
