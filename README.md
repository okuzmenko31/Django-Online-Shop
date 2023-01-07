## Python + Django project of web store

- **python 3.11**
- **Django 4.1.3**
- **postgres 15.1**

## Clone Repository & Install Packages

```
git clone https://github.com/okuzmenko31/RvShop-Online-Store-.git```
pip install req.txt
```

## Setup Virtualenv

````
virtualenv venv
source venv/Scrpits/activate
````

## Running RabbitMQ and Celery

- **Run the Docker ([Install](https://docs.docker.com/get-docker/) if you don't have it)**
- **Run the RabbitMQ with the command in console:**
````
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
````
- **Run the Celery with the command:**
```
celery -A RvShop worker --loglevel=info -P eventlet
```

## About email connection in settings.py

- **For correct work of sending letters, you need to replace
  available email to yours and write you password instead of
  available. I used connection with gmail.com, if you want to
  connect with it [click here](https://support.google.com/mail/answer/7126229?hl=ru)
  for more information about it.**
- **Also, my gmail password was hidden with ConfiParser, you can
  read the documentation [here](https://docs.python.org/3/library/configparser.html#module-configparser)**

## Migrate & Start Server

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
