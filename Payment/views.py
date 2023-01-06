from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from Order.models import Order
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from Cart.cart import Cart


@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    order.paid = True
    order.save()
    context = {
        'order': order,
    }
    return render(request, template_name='Payment/payment_done.html', context=context)


@csrf_exempt
def payment_cancel(request):

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    order.delete()
    return render(request, 'Payment/payment_cancel.html')


def payment_process(request):
    cart = Cart(request)

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f'{order.order_total_price}',
        'item_name': f'Order {order.id}',
        'invoice': f'{order.id}',
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("payment_done")}',
        'cancel_return': f'http://{host}{reverse("payment_cancel")}',
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    context = {
        'order': order,
        'form': form,
        'cart': cart,
    }
    return render(request, template_name='Payment/payment_process.html', context=context)
