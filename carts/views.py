from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from products.models import ProductVariant

# Create your views here.
def carts_list(request):
    cart = Cart(request)
    return render(request, 'carts/carts_list.html', {'carts' : cart})

def carts_add(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant ,id=variant_id)
    quantity=int(request.GET.get('quantity', request.POST.get('quantity', 1)))
    cart.add(variant=variant, quantity=quantity)
    return redirect('carts:list')

def carts_remove(request, variant_id):
    cart = Cart(request)
    vartant = get_object_or_404(ProductVariant, id=variant_id)

    cart.remove(vartant)
    return redirect('carts:list')
