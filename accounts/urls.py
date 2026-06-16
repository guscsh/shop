from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

# URL names in this file are referenced from templates using
# {% url 'accounts:<name>' %}. Keep names stable when possible.
urlpatterns = [
    # Auth
    path('register/', views.register_view, name="register"),
    path('login/', LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True
    ), name="login"),
    path('logout/', LogoutView.as_view(next_page='pages:index'), name="logout"),

    # Member center
    path('profile/', views.profile, name="profile"),
    path('dashboard/', views.AccountDashboard.as_view(), name="dashboard"),
    path('orders/', views.order_history, name="orders"),
    path('favourites/', views.favourites, name="favourites"),

    # Wishlist toggle endpoint (used by product page button/form)
    path('favourites/<int:product_id>/', views.toggle_favourite, name="toggle_favourite"),
]