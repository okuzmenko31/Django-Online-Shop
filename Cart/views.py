from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from Products.models import Product
from .cart import Cart


class CartDetail(View):
    """Detail view of the basket"""

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        return render(self.request, 'Cart/detail.html', {'cart': cart})


class CartAdd(View):
    """Detail view of the cart"""

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.add(product=product)
        return redirect('cart')


class CartRemove(View):
    """View for removing product from the basket"""

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.remove(product)
        return redirect('cart')


class CartAddQuantity(View):
    """View for increasing product quantity in the cart"""

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.add_quantity(product)
        return redirect('cart')


class CartMinusQuantity(View):
    """View for decreasing product quantity in the cart"""

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.minus_quantity(product)
        return redirect('cart')
