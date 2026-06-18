from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, ProfileUpdateForm, CustomPasswordForm
from users.models import UserProfile
from products.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from PIL import Image
from orders.models import Order

# ---------------------------------------------------------------------------
# Accounts entry points
# ---------------------------------------------------------------------------

def register_view(request):
    """Register a new user and log them in immediately."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("pages:index")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# ---------------------------------------------------------------------------
# Profile and account pages
# ---------------------------------------------------------------------------

@login_required
def profile(request):
    """
    Update profile information and (optionally) change password.

    Notes for learning:
    - User basic fields (first_name/last_name) live on auth User.
    - Extra fields (phone/avatar) live on UserProfile.
    - We validate profile form and password form independently.
    """
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    profile_form = ProfileUpdateForm(instance=profile, user=user)
    pwd_form = CustomPasswordForm(user)

    if request.method == "POST":
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile, user=user
        )
        pwd_form = CustomPasswordForm(user, request.POST)

        # If new_password1 has value, we treat this request as password-change attempt.
        password_attempted = bool(request.POST.get('new_password1'))
        profile_ok = profile_form.is_valid()
        password_ok = pwd_form.is_valid() if password_attempted else True
        
        if profile_ok and password_ok:
            # 1) Update auth User fields.
            user.first_name = profile_form.cleaned_data['first_name']
            user.last_name = profile_form.cleaned_data['last_name']
            user.save()

            # 2) Update profile fields.
            profile = profile_form.save(commit=False)
            profile.user = user

            # 3) If avatar exists, apply crop/resize before final render.
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
                    # Keep request successful even if image processing fails.
                    pass
            else:
                profile.save()

            # 4) Optional password change.
            if password_attempted:
                pwd_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Profile and password updated successfully.')
            else:
                messages.success(request, 'Profile updated successfully.')
            
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')

    context = {
        'profile_form': profile_form, 
        'pwd_form': pwd_form, 
        'user': user, 
        'profile': profile 
    }
    return render(request, "accounts/profile.html", context)    


class AccountDashboard(LoginRequiredMixin, TemplateView):
    """Simple member dashboard."""
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user

        profile, _ = UserProfile.objects.get_or_create(user=user)

        context["point_balance"] = profile.points
        context["order_history"] = Order.objects.filter(user=user).count()
        context["total_favourites"] = profile.favorites.count()
        return context


@login_required
def order_history(request):
    """會員訂單列表：只顯示當前登入使用者的訂單。"""
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related('items')
        .select_related('payment')
        .order_by('-created_at')
    )
    return render(request, 'accounts/orders.html', {
        'order_list': orders,
        'user': request.user,
    })


@login_required
def order_detail(request, order_no):
    """訂單詳情：僅允許訂單擁有者查看。"""
    order = get_object_or_404(
        Order.objects.select_related('payment').prefetch_related('items'),
        order_no=order_no,
        user=request.user,
    )
    return render(request, 'accounts/order_detail.html', {
        'order': order,
        'user': request.user,
    })


@login_required
def favourites(request):
    """Render member favourites (wishlist) page."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    fav_list = profile.favorites.all()
    return render(request, "accounts/favourites.html", {
        "fav_list": fav_list,
        "user": request.user
    })

@login_required
def toggle_favourite(request, product_id):
    """Toggle product in/out of current user's favourites."""
    profile = request.user.profile
    product = get_object_or_404(Product, id=product_id)
    
    if product in profile.favorites.all():
        profile.favorites.remove(product)
        status = 'removed'
    else:
        profile.favorites.add(product)
        status = 'added'
    
    # Return JSON for AJAX clients; otherwise redirect back.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'product_id': product_id})
    else:
        return redirect(request.META.get('HTTP_REFERER', 'products:list'))