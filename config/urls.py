"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from accounts.views import register_view,logout_view

urlpatterns = [
    path('', include('pages.urls', namespace='pages')),
    path('Products/', include('products.urls', namespace='products')), 
    path('admin/', admin.site.urls),
    # Auth Routes
    path('register/', register_view, name="register"),
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout/', logout_view, name="logout"),
    path('accounts/', include('accounts.urls', namespace='accounts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
