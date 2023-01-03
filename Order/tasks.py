from RvShop.celery import app
from django.core.mail import send_mail
from .models import Order, OrderItem
from Cart.cart import Cart


@app.task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'{order.name} - Ви успішно зробили замовлення! Номер вашого замовлення: {order.id}'
    message = f'Шановний {order.name} {order.last_name} - Ви успішно зробили замовлення на RvShop. Дякуємо Вам за те, '\
              f'що Ви вибрали саме нас. Номер Вашого замовлення: {order.id}. Очікуйте на дзвінок для уточнення ' \
              f'інформації, чекаємо Вас ще!'
    mail_sent = send_mail(subject, message, 'kuzmenkowebdev@gmail.com', [order.email])
    return mail_sent
