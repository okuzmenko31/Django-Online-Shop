from django.shortcuts import render, redirect
from django.views import View
from .forms import OrderCreateForm
from .models import *
from Cart.cart import Cart
from .tasks import order_created


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

            if order.order_total_price == 0 and order.order_total_price_usd == 0:
                # If order total price os 0, user will be redirected
                # to the payment done page, because he paid with his bonuses.

                try:
                    order_created.delay(order.id)
                except (Exception,):
                    print('Celery is not working now')
                return redirect('payment_done')
            else:
                return redirect('payment_process')
