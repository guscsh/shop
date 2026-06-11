from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, ProfileUpdateForm, CustomPasswordForm
from .models import Order
from users.models import UserProfile
from django.contrib.auth.decorators import login_required
from PIL import Image
import os


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("pages:index")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# Logout
def logout_view(request):
    logout(request)
    next_url = request.GET.get('next')
    is_safe = url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    )
    if is_safe and next_url:
        return redirect(next_url)
    return redirect('pages:index')


# Get or create user profile
def get_or_create_profile(user):
    profile, created = UserProfile.objects.get_or_create(user=user)
    return profile


# Profile page
def profile(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('accounts:login')

    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile_form = ProfileUpdateForm(instance=profile, user=user)
    pwd_form = CustomPasswordForm(user)

    if request.method == "POST":
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile, user=user
        )
        pwd_form = CustomPasswordForm(user, request.POST)

        if profile_form.is_valid():
            # Update user first/last name
            user.first_name = profile_form.cleaned_data['first_name']
            user.last_name = profile_form.cleaned_data['last_name']
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # Avatar crop & resize
            if profile.avatar:
                profile.save()
                img_path = profile.avatar.path
                try:
                    img = Image.open(img_path).convert("RGB")
                    x = int(profile.crop_x)
                    y = int(profile.crop_y)
                    w = int(profile.crop_w)
                    h = int(profile.crop_h)

                    if w > 0 and h > 0:
                        img = img.crop((x, y, x + w, y + h))
                    img = img.resize((300, 300), Image.Resampling.LANCZOS)
                    img.save(img_path, "JPEG", quality=85)
                except Exception:
                    pass
            else:
                profile.save()

            # Change password
            if request.POST.get('new_password1'):
                if pwd_form.is_valid():
                    pwd_form.save()
                    update_session_auth_hash(request, user)

            return redirect('accounts:profile')

    context = {
        'profile_form': profile_form,
        'pwd_form': pwd_form,
        'user': user,
        'profile': profile
    }
    return render(request, "accounts/profile.html", context)


# Dashboard
class AccountDashboard(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user

        # Auto create profile if missing (fix User has no profile error)
        profile, _ = UserProfile.objects.get_or_create(user=user)

        context["point_balance"] = profile.points
        context["vip_level"] = profile.vip_level_display
        context["order_history"] = Order.objects.filter(user=user).count()
        context["total_favourites"] = profile.favorites.count()
        return context


# Order History
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, "accounts/orders.html", {
        "order_list": orders,
        "user": request.user
    })


# Favourites (use UserProfile M2M field)
@login_required
def Favourites(request):
    profile = request.user.profile
    fav_list = profile.favorites.all()
    return render(request, "accounts/Favourites.html", {
        "fav_list": fav_list,
        "user": request.user
    })