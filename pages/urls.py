from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog/post/', views.blog_post, name='blog_post'),
    path('shop/', views.shop_list, name='shop_list'), 
]

handler404 = 'pages.views.custom_404'
