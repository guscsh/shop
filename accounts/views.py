from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, ProfileUpdateForm, CustomPasswordForm

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("pages:index")
    else:
        form = RegisterForm()
    return render(request,"accounts/register.html",{"form":form})

# Logout
def logout_view(request):
    logout(request)
    next = request.GET.get('next')             
    is_safe = url_has_allowed_host_and_scheme( 
        url=request.GET.get('next'),           
        allowed_hosts={request.get_host()},    
        require_https=request.is_secure()  
    )
    if is_safe:                                
        return redirect(next)
    else:
        return redirect('pages:index')    

# Profile
def profile(request):
    user = request.user
    # Login protection
    if not user.is_authenticated:
        return redirect('accounts:login')

    profile_form = ProfileUpdateForm(instance=user)
    pwd_form = CustomPasswordForm(user)

    if request.method == "POST":
        # Update personal info
        if 'profile_submit' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('accounts:profile')

        # Update password
        if 'pwd_submit' in request.POST:
            pwd_form = CustomPasswordForm(user, request.POST)
            # Allow empty password (no change)
            if not request.POST.get('new_password1'):
                return redirect('accounts:profile')
            if pwd_form.is_valid():
                pwd_form.save()
                # Keep user logged in after password change
                update_session_auth_hash(request, user)
                return redirect('accounts:profile')

    context = {
        'profile_form': profile_form,
        'pwd_form': pwd_form,
        'user': user
    }
    return render(request, "accounts/profile.html", context)

# Dashboard  
class AccountDashboard(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        #context demo
        context["point_balance"] = 1
        context["order_history"] = 1
        context["total_wishlist"] = 1
        return context