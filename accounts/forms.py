from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

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
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# Custom password change form (leave blank = no change)
class CustomPasswordForm(PasswordChangeForm):
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