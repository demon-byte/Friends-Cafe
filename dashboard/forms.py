from django import forms
from menu.models import Category, MenuItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'description', 'price', 'image', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }