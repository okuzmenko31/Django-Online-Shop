from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from Order.models import Order, OrderItem
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from Cart.cart import Cart
from Order.tasks import order_created


@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    order_created.delay(order.id)

    items = OrderItem.objects.filter(order=order)

    del request.session['order_id']
    request.session.modified = True

    order.paid = True
    order.save()

    context = {
        'order': order,
        'items': items,
    }
    return render(request, template_name='Payment/payment_done.html', context=context)


@csrf_exempt
def payment_cancel(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    del request.session['order_id']
    request.session.modified = True

    order.delete()
    return render(request, 'Payment/payment_cancel.html')


def payment_process(request):
    cart = Cart(request)

    order_id = request.session.get('order_id')

    if order_id:

        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        count_items = ''

        items_lst = []

        for item in order_items:
            items_lst.append(str(item.product.name))

        order_items_count = len(items_lst)

        count_items += ''.join(f'count of products in order: {order_items_count}')

        host = request.get_host()

        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': f'{order.order_total_price_usd}',
            'item_name': f'Order #{order.id}, \n\n{count_items}',
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
            'order_items': order_items,
        }

        return render(request, template_name='Payment/payment_process.html', context=context)
    else:
        return redirect('all_products')
