from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from users.models import UserProfile

# ---------------------------------------------------------------------------
# Auth forms
# ---------------------------------------------------------------------------

class RegisterForm(UserCreationForm):
    """Registration form based on Django User model."""
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # Apply Bootstrap class to all generated fields.
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})

class CustomLoginForm(AuthenticationForm):
    """Login form with Bootstrap styling only."""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})

# ---------------------------------------------------------------------------
# Profile forms
# ---------------------------------------------------------------------------

class ProfileUpdateForm(forms.ModelForm):
    """
    Update profile and basic user data in one screen.

    Note:
    - first_name/last_name/email belong to auth User.
    - phone/avatar/crop_* belong to UserProfile.
    """
    first_name = forms.CharField(
        max_length=150, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    last_name = forms.CharField(
        max_length=150, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}),
        disabled=True
        )
    phone = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'd-none', 'id': 'avatar-input'}),
        allow_empty_file=False
    )
    
    crop_x = forms.FloatField(widget=forms.HiddenInput())
    crop_y = forms.FloatField(widget=forms.HiddenInput())
    crop_w = forms.FloatField(widget=forms.HiddenInput())
    crop_h = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = ['phone', 'avatar', 'crop_x', 'crop_y', 'crop_w', 'crop_h']

    def __init__(self, *args, **kwargs):
        # `user` is passed from view to prefill User-owned fields.
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

class CustomPasswordForm(PasswordChangeForm):
    """
    Password form used in profile page.

    All fields are optional at form-level because password change itself is
    optional in that page. View logic decides when to validate/save it.
    """
    old_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    new_password1 = forms.CharField(
        label="New password (leave blank to leave unchanged)",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
