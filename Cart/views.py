from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from Products.models import Product
from .cart import Cart


class CartAdd(View):

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.add(product=product)
        return redirect('cart')


class CartRemove(View):

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.remove(product)
        return redirect('cart')


class CartAddQuantity(View):

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.add_quantity(product)
        return redirect('cart')


class CartMinusQuantity(View):

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart.minus_quantity(product)
        return redirect('cart')


class CartDetail(View):

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        return render(self.request, 'Cart/detail.html', {'cart': cart})
