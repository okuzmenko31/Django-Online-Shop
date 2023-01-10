from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import *
from Cart.cart import Cart
from .tasks import order_created


def order_create(request):
    """Order creating"""
    cart = Cart(request)

    if len(cart) > 0:
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save()  # assign the newly created order to the order variable

                for item in cart:
                    """Loop through all the objects in cart and creating new instance of model OrderItem"""

                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])

                cart.clear()

                request.session['order_id'] = order.id
                return redirect('payment_process')

        else:
            form = OrderCreateForm()  # just returning the order form with no data

        context = {
            'cart': cart,
            'form': form,
        }
        return render(request, 'Order/create_order.html', context=context)
    else:
        return redirect('all_products')
