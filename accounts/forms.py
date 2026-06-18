from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from users.models import UserProfile

# ---------------------------------------------------------------------------
# Register Form
# ---------------------------------------------------------------------------

class RegisterForm(UserCreationForm):
    """Registration form based on Django User model."""
    # Add an extra email field (because the built-in registration usually only has username and password).
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        # Define which fields this form should include (Password 1 is for input, Password 2 is for confirming the password)
        fields = ["username","email","password1","password2"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # Apply "form-control" Bootstrap class to all generated fields.
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})

# ---------------------------------------------------------------------------
# Custom Login Form
# ---------------------------------------------------------------------------
class CustomLoginForm(AuthenticationForm):
    """Login form with Bootstrap styling only."""
    # Simply add a visual style to the "Account" and "Password" input fields using a loop.
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})

# ---------------------------------------------------------------------------
# Profile Update Form 
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
    # Email is set to readonly and disabled.
    # To prevent members from arbitrarily changing their linked primary email address, which could lead to account disputes.
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}),
        disabled=True
        )
    # Define the phone number field belonging to UserProfile
    phone = forms.CharField(
        max_length=20, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    # Avatar Upload: Add 'd-none' to hide the unsightly default upload button, so it can be paired with custom image click box on the front end.
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'd-none', 'id': 'avatar-input'}),
        allow_empty_file=False
    )
    # HiddenInput: Used to quietly receive image cropping coordinates from a front-end JavaScript cropping tool (such as Cropper.js).
    # The X, Y axes, length and width will be silently sent to the backend for processing by Pillow.
    crop_x = forms.FloatField(widget=forms.HiddenInput())
    crop_y = forms.FloatField(widget=forms.HiddenInput())
    crop_w = forms.FloatField(widget=forms.HiddenInput())
    crop_h = forms.FloatField(widget=forms.HiddenInput())

    # Modify the UserProfile form
    class Meta:
        model = UserProfile
        fields = ['phone', 'avatar', 'crop_x', 'crop_y', 'crop_w', 'crop_h']

    def __init__(self, *args, **kwargs):
        # `user` is passed from view.py to prefill User-owned fields.
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            ## Use the current logged-in user's existing first name, last name, and email address as default values ​​and fill them into the input box.
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

# ---------------------------------------------------------------------------
# Custom Password Form 
# All required fields are set to False (not required).
# The backend only initiates the verification process when a new password is entered.
# ---------------------------------------------------------------------------
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
