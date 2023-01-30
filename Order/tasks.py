from django.template.loader import render_to_string

from RvShop.celery import app
from django.core.mail import send_mail
from .models import Order, OrderItem
from Cart.cart import Cart


@app.task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    html_msg = {
        'success_msg': f'{order.name} - You successfully placed your order!',
        'order_num': f'Number of order: {order.id}.',
        'order_price_uah': f'Total price of order in UAH: {order.order_total_price_view}.',
        'order_price_usd': f'Total price of order in USD: {order.order_total_price_usd_view}.',
        'last_msg': 'Thanks for order. Wait for call from our manager.'
    }

    html_message = 'Order/created_order.html'
    ht_message = render_to_string(html_message, html_msg)
    subject = f'RvShop - You successfully placed your order!'
    message = f'Шановний {order.name} {order.last_name} - Ви успішно зробили замовлення на RvShop. Дякуємо Вам за те, ' \
              f'що Ви вибрали саме нас. Номер Вашого замовлення: {order.id}. Очікуйте на дзвінок для уточнення ' \
              f'інформації, чекаємо Вас ще!'
    mail_sent = send_mail(subject, message, 'kuzmenkowebdev@gmail.com', [order.email],
                          html_message=ht_message)  # replace email to yours
    return mail_sent
