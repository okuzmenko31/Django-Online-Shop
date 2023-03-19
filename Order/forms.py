from django import forms

from Coupons.models import Coupons
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'last_name', 'surname',
                  'phone', 'email', 'address', 'country', 'city', 'post_office',
                  'coupon', 'activate_bonuses']
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
            'coupon': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, request, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.request = request

        if not self.request.user.is_authenticated:
            """If user is not authenticated this fields
             will be deleted from the form."""
            del self.fields['coupon']
            del self.fields['activate_bonuses']
        else:
            """User can choose only active coupon"""
            self.fields['coupon'].queryset = Coupons.objects.filter(is_active=True)
