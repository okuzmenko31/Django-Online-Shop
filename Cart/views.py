from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from Products.models import Product
from .cart import Cart


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart')


def cart_add_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add_quantity(product)
    return redirect('cart')


def cart_minus_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.minus_quantity(product)
    return redirect('cart')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'Cart/detail.html', {'cart': cart})
