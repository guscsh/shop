from django.urls import path
from . import views

app_name = 'carts' 

urlpatterns = [
    path('', views.carts_list, name='list'),
    path('add/(int:variant_id)/', views.carts_add, name='add'),
    path('remove/<int:variant_id>/', views.carts_remove, name='remove')
]