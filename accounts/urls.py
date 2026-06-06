from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=True), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile, name="profile"),
]