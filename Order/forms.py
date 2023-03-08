from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'last_name', 'phone', 'email', 'address', 'post_office', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your name"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your surname"}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your phone"}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your email"}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your address"}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write you post office"}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write you city or town"}),
        }
