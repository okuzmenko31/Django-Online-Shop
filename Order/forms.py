from django import forms
from Cart.cart import Cart
from Coupons.models import Coupons
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'last_name', 'surname',
                  'phone', 'email', 'address', 'country', 'city', 'post_office',
                  'coupon', 'use_bonuses']
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
        cart = Cart(self.request)
        subcategories_list = []  # list for subcategories of all products in cart

        for item in cart:
            # We fill the list with subcategories
            # of products in the cart.

            subcategories_list.append(item['product'].subcategory)

        if not self.request.user.is_authenticated:
            # If user is not authenticated this fields
            # will be deleted from the form.

            del self.fields['coupon']
            del self.fields['use_bonuses']
        else:
            # User can choose only active coupon and
            # if subcategory of coupons is in list of
            # subcategories of products in cart.

            coupons = Coupons.objects.filter(user=self.request.user)
            if coupons:
                self.fields['coupon'].queryset = Coupons.objects.filter(is_active=True,
                                                                        subcategory__in=subcategories_list)
            else:
                del self.fields['coupon']

            if self.request.user.bonuses_balance is 0 and self.request.user.bonuses_balance_usd is 0:
                """We don't show field with bonuses using if user's
                bonuses balance is 0."""
                del self.fields['use_bonuses']
