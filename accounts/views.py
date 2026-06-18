from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, ProfileUpdateForm, CustomPasswordForm
from users.models import UserProfile
from products.models import Product
from django.http import JsonResponse
from django.contrib import messages
from PIL import Image

# ---------------------------------------------------------------------------
# Resigner View
# ---------------------------------------------------------------------------

def register_view(request):
    """Register a new user and log them in immediately."""
    if request.method == "POST": # When a user clicks "Submit Registration Form"
        form = RegisterForm(request.POST)
        if form.is_valid(): # Verify information (password length, email address consistency)
            user = form.save() # Save new user to database
            login(request, user) # Convenient design: No need to re-enter information, automatically logs the user after registration
            return redirect("pages:index") # Redirect to homepage
    else: # When a user simply clicks on the registration page (GET request)
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# ---------------------------------------------------------------------------
# Personal Profile and Password Change (profile)
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
    # Ensure that the user has a "UserProfile" object. If not, create one immediately to avoid system crashes.
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    # Render two blank/preset forms by importing existing data (Instance).
    profile_form = ProfileUpdateForm(instance=profile, user=user)
    pwd_form = CustomPasswordForm(user)

    # Receive new information, new passwords, and uploaded profile picture files (request.FILES) from the user.
    if request.method == "POST":
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=profile, user=user
        )
        pwd_form = CustomPasswordForm(user, request.POST)

        # If new_password1 has value, we treat this request as password-change attempt.
        # If he doesn't intend to change his password, the password verification will be passed directly as True; only if he intends to change it will pwd_form.is_valid() be executed for verification.
        password_attempted = bool(request.POST.get('new_password1'))
        profile_ok = profile_form.is_valid()
        password_ok = pwd_form.is_valid() if password_attempted else True
        
        if profile_ok and password_ok:
            # 1) Update auth User fields.
            user.first_name = profile_form.cleaned_data['first_name']
            user.last_name = profile_form.cleaned_data['last_name']
            user.save()

            # 2) Update UserProfile fields.
            profile = profile_form.save(commit=False)
            profile.user = user

            # 3) Automatic image cropping and compression
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
                        # If the frontend provides the coordinates of the cropping box (w > 0 and h > 0), then crop the image.
                        img = img.crop((x, y, x + w, y + h))
                    # Resize images to a standard 300x300 pixels and render in high quality (LANCZOS).
                    img = img.resize((300, 300), Image.Resampling.LANCZOS)
                    img.save(img_path, "JPEG", quality=85)
                except Exception:
                    # Keep request successful even if image processing fails.
                    pass
            else:
                profile.save()

            # 4) Optional password change.
            # After changing the password, the old login credentials will become invalid. Update the credentials so that users do not need to log in again.
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

# ---------------------------------------------------------------------------
# Member Dashboard, Orders and Wishlist pages
# ---------------------------------------------------------------------------
class AccountDashboard(LoginRequiredMixin, TemplateView):
    """Simple member dashboard."""
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user

        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Retrieve the points and number of favorite items from the backend and pass them to the HTML for display.
        context["point_balance"] = profile.points 
        context["order_history"] = 0
        context["total_favourites"] = profile.favorites.count()
        return context


@login_required
def order_history(request):
    """Order list placeholder page before orders app integration."""
    orders = []
    return render(request, "accounts/orders.html", {
        "order_list": orders,
        "user": request.user
    })


@login_required
def favourites(request):
    """Render member favourites (wishlist) page."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    fav_list = profile.favorites.all() #Find out all my favorite items
    return render(request, "accounts/favourites.html", {
        "fav_list": fav_list,
        "user": request.user
    })

# ---------------------------------------------------------------------------
# Toggle Favorite items
# ---------------------------------------------------------------------------
@login_required
def toggle_favourite(request, product_id):
    """Toggle product in/out of current user's favourites."""
    profile = request.user.profile
    product = get_object_or_404(Product, id=product_id)
    
    # Check if this item is already in the list
    if product in profile.favorites.all():
        profile.favorites.remove(product)
        status = 'removed' # Exists ➔ Remove
    else:
        profile.favorites.add(product) 
        status = 'added' # Does not exist ➔ Join
    
    # Return JSON for AJAX clients; otherwise redirect back. (JsonResponse)
    # After clicking the heart, the button changes color automatically, but the webpage doesn't need to be refreshed at all.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status, 'product_id': product_id})
    else:
        return redirect(request.META.get('HTTP_REFERER', 'products:list'))