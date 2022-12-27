from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'last_name', 'phone', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введiть Ваше iм'я"}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введiть Вашу фамiлiю"}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введiть Ваш телефон"}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введiть Ваш email"}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введiть Вашу адресу"}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введiть Ваш поштовий код"}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Введiть Ваше мiсто"}),
        }
