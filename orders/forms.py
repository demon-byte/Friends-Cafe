from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_notes', 'payment_method']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
            'delivery_notes': forms.Textarea(attrs={'rows': 2}),
            'payment_method': forms.RadioSelect(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].widget.attrs.update({'class': 'flex flex-col space-y-2'})