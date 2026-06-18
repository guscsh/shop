from django.urls import path
from . import views

app_name = 'orders' 

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/place/', views.place_order, name='place_order'),
    path('success/<str:order_no>/', views.order_success, name='success'),
    path('failed/', views.order_failed, name='failed'),
]