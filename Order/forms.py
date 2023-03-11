from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'last_name', 'surname', 'phone', 'email', 'address', 'country', 'city', 'post_office']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your name"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your last name"}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your surname"}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your phone"}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your email"}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your address"}),
            'post_office': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your post office"}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your city or town"}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Write your city or town"}),
        }
