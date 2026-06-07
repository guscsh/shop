from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import NewsletterSubscriber 
from django.contrib import messages

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

def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        consented = request.POST.get("marketing") == "on"
        # Check if the mailbox already exists
        if NewsletterSubscriber.objects.filter(email=email).exists():
            messages.error(request, "This email is already subscribed!")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        # Save subscriber
        if email and consented:
            NewsletterSubscriber.objects.get_or_create(email=email, defaults={"consented": True})
            messages.success(request, "Subscribed successfully!")
    return redirect('/')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def test(request):
    return render(request, 'pages/test.html')