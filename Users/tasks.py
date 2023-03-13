from django.core.mail import send_mail

from OnlineShop.celery import app


@app.task
def send_password_reset_mail(subject, email, msg_html):
    send_mail(subject, 'link', 'kuzmenkowebdev@gmail.com', [email], fail_silently=False,
              html_message=msg_html)
