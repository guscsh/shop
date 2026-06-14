from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from users.models import UserProfile

# Register Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control"}))
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})

# Custom Login Form
class CustomLoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class":"form-control"})

# Profile update form
class ProfileUpdateForm(forms.ModelForm):
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
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

class CustomPasswordForm(PasswordChangeForm):
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
