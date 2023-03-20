from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from paypal.standard.forms import PayPalPaymentsForm
from Order.models import Order, OrderItem
from django.conf import settings
from Cart.cart import Cart
from Order.tasks import order_created
from Products.services import get_discount, get_price_in_usd
from .utils import CSRFExemptMixin
from Order.services import generate_code
from .services import create_coupon


class PaymentDone(CSRFExemptMixin, View):

    def get(self, *args, **kwargs):
        order_id = self.request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        try:
            order_created.delay(order.id)
        except (Exception,):
            print('Celery is not working now')

        if self.request.user.is_authenticated:

            user_bonuses = 0
            user_bonuses_usd = 0

            if order.order_bonuses and order.order_bonuses_usd:
                """
                If order have bonuses, we add them
                to user's bonuses balance.
                """
                user_bonuses += order.order_bonuses
                user_bonuses_usd += order.order_bonuses_usd

                self.request.user.bonuses_balance += user_bonuses
                self.request.user.bonuses_balance_usd += user_bonuses_usd
                self.request.user.save()

            create_coupon(order.user)  # a function is called to create a coupon

        items = OrderItem.objects.filter(order=order)

        del self.request.session['order_id']
        self.request.session.modified = True

        order.paid = True
        order.save()

        context = {
            'order': order,
            'items': items,
        }
        return render(self.request, template_name='Payment/payment_done.html', context=context)


class PaymentCancel(CSRFExemptMixin, View):

    def get(self, *args, **kwargs):
        order_id = self.request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)

        del self.request.session['order_id']
        self.request.session.modified = True

        order.delete()
        return render(self.request, 'Payment/payment_cancel.html')


class PaymentProcess(CSRFExemptMixin, View):
    def get(self, *args, **kwargs):
        cart = Cart(self.request)
        order_id = self.request.session.get('order_id')

        if order_id:
            order = get_object_or_404(Order, id=order_id)
            order_items = OrderItem.objects.filter(order=order)
            subcategories_list = []  # list for subcategories of all products in order

            for item in order_items:
                # We fill the list with subcategories
                # of products in the order.

                subcategories_list.append(item.product.subcategory)

            if self.request.user.is_authenticated:
                if order.coupon:

                    order.coupon.is_active = False
                    order.coupon.save()

                    if order.coupon.subcategory in subcategories_list:
                        # If subcategory of coupon is equal to
                        # subcategory of one of products in order, the
                        # user will receive discount for this order.

                        order_total_price = order.order_total_price
                        order.order_total_price = get_discount(order_total_price, order.coupon.discount)
                        order.order_total_price_usd = get_price_in_usd(order.order_total_price)

                if order.use_bonuses:
                    usr_bonuses = self.request.user.bonuses_balance
                    usr_bonuses_usd = self.request.user.bonuses_balance_usd

                    if usr_bonuses < order.order_total_price and usr_bonuses_usd < order.order_total_price_usd:
                        order.order_total_price -= usr_bonuses
                        order.order_total_price_usd -= usr_bonuses_usd
                        self.request.user.bonuses_balance = 0
                        self.request.user.bonuses_balance_usd = 0
                        self.request.user.save()

                order.save()

            count_items = ''

            items_lst = []

            for item in order_items:
                items_lst.append(str(item.product.name))

            order_items_count = len(items_lst)
            count_items += ''.join(f'count of products in order: {order_items_count}')

            host = self.request.get_host()

            paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': f'{order.order_total_price_usd}',
                'item_name': f'Order #{order.id}, \n\n{count_items}',
                'invoice': f'{generate_code()}{order_id}',
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
            return render(self.request, template_name='Payment/payment_process.html', context=context)
        else:
            return redirect('all_products')
