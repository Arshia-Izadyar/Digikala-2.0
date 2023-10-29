from .models import Provider, Review, ReviewImage
from django import forms


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ("provider_name", "address", "working_perm_id", "owner_national_code")
        

class ReviewForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Review
        fields = ['rating', 'review', 'recommend', 'is_anon']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].widget.attrs.update({'accept': 'image/*'})