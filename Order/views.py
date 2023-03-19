from django.shortcuts import render, redirect
from django.views import View
from .forms import OrderCreateForm
from .models import *
from Cart.cart import Cart


class OrderCreate(View):

    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        form = OrderCreateForm(self.request)

        return render(self.request, 'Order/create_order.html', {'cart': cart, 'form': form})

    def post(self, *args, **kwargs):
        cart = Cart(self.request)
        form = OrderCreateForm(self.request, self.request.POST)
        user = self.request.user

        if form.is_valid():
            order = form.save(commit=False)

            if user.is_authenticated:
                order.user = user
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         price_usd=item['price_usd'],
                                         quantity=item['quantity'])
            cart.clear()

            self.request.session['order_id'] = order.id
            return redirect('payment_process')
