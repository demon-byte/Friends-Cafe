from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'default_address', 'additional_addresses']
        widgets = {
            'default_address': forms.Textarea(attrs={'rows': 3}),
            'additional_addresses': forms.Textarea(attrs={'rows': 3}),
        }