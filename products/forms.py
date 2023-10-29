from .models import Provider
from django import forms


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ("provider_name", "address", "working_perm_id", "owner_national_code")
        
        