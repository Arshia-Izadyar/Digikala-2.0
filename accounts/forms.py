from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import gettext as _
from .models import User, Address


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("phone_number",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields
        
class UserLoginForm(forms.Form):
    email_phone = forms.CharField(max_length=50, min_length=6, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    



class AddressCreationForm(forms.ModelForm):
    class Meta():
        model = Address
        fields = ("address", "zip_code", "city", "phone_number", "receiver_name")

