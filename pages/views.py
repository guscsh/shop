from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def blog(request):
    return render(request, 'pages/blog.html')

def blog_post(request):
    return render(request, 'pages/post-standard.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)
