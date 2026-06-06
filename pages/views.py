from django.shortcuts import render
from .models import Product

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def blog(request):
    return render(request, 'pages/blog.html')

def blog_post(request):
    return render(request, 'pages/post-standard.html')

def shop_list(request):
    selected_color = request.GET.get('color', '')
    selected_category = request.GET.get('category', '')
    min_price = request.GET.get('min', 0)
    max_price = request.GET.get('max', 300)
    products = Product.objects.all()
    if selected_color:
        products = products.filter(color=selected_color)
    if selected_category:
        products = products.filter(category__name=selected_category)
    products = products.filter(
        price__gte=min_price,
        price__lte=max_price
    )
    total_products = Product.objects.count()
    context = {
        'products': products,
        'total_products': total_products,
        'selected_color': selected_color,
        'max_p': max_price,
    }
    return render(request, 'pages/shop-list.html', context)

def custom_404(request, exception):
    return render(request, '404.html', status=404)
