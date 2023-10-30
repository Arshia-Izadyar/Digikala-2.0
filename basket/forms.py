from django import forms
from products.models import Product
from .models import Basket


class AddToBasketForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects, widget=forms.HiddenInput())
    quantity = forms.IntegerField(initial=1)
    
    def save_to_basket(self, basket):
       
        product = self.cleaned_data["product"]
        quantity = self.cleaned_data["quantity"]
        basket.add_to_basket(product=product, amount=quantity)
        return basket
    
