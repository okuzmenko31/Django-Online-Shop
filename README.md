**Python + Django project of web store**

- python 3.11
- Django 4.1.3
- postgres 15.1

**Installing**

- pip install req.txt

**Running RabbitMQ and Celery**

- Run the Docker (Install if you don't have it)
- Run the RabbitMQ with the
<a href="https://www.rabbitmq.com/download.html">command</a> in console
- Run the Celery with the command (celery -A RvShop worker --loglevel=info -P eventlet)

**About email connection in settings.py**

- For correct work of sending letters, you need to replace 
available email to yours and write you password instead of
available. I used connection with gmail.com, if you want to
connect with it <a href="https://support.google.com/mail/answer/7126229?hl=ru">click here</a> 
for more information about it.

