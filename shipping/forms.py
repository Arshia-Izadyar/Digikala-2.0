from django import forms

from .models import Shipping
from accounts.models import Address

class ShippingForm(forms.ModelForm):
    sending_date = forms.DateField(required=True)
    class Meta:
        model = Shipping
        fields = ("sending_date", "delivery_method", "user_address")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ShippingForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["user_address"].queryset = Address.objects.filter(user=user)