from django.core.mail import send_mail
from django.conf import settings
from OnlineShop.celery import app


@app.task
def send_password_reset_mail(subject, email, msg_html):
    send = send_mail(subject, 'link', 'kuzmenkowebdev@gmail.com', [email], fail_silently=False,
                     html_message=msg_html)
    return send


@app.task
def change_email_success_mail(username, email):
    subject = f'{username} - You successfully confirmed new email!'
    message = 'Thank you for being with us!\n' \
              'Sincerely, OnlineShop team.'
    send = send_mail(subject, message, str(settings.EMAIL_HOST_USER), [email])
    return send
