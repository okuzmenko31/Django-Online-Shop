## Python + Django project of web store

- **python 3.11**
- **Django 4.1.3**
- **postgres 15.1**

## Clone Repository

```
git clone https://github.com/okuzmenko31/RvShop-Online-Store-.git
```

## Go to project directory

```
cd RvShop-Online-Store
```

## Setup Virtualenv

````
virtualenv venv
source venv/Scripts/activate
````

## Install packages

```
pip install -r req.txt
```

## Running RabbitMQ

- **Run the Docker ([Install](https://docs.docker.com/get-docker/) if you don't have it)**
- **Run the RabbitMQ with the command in cmd or linux console:**
````
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
````

## Change DB connection in settings.py
### Connection to SQLite3

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Connection to PostgreSQL

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'host',
        'PORT': 5433
    }
}
```

## Migrate & Start Server

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Run Celery

```
celery -A RvShop worker --loglevel=info -P eventlet
```

## About email connection in settings.py

- **For correct work of sending letters, you need to replace
  available email to yours and write you password instead of
  available. I used connection with gmail.com, if you want to
  connect with it [click here](https://support.google.com/mail/answer/7126229?hl=ru)
  for more information about it.**
- **Also, my gmail password was hidden with ConfigParser, you can
  read the documentation [here](https://docs.python.org/3/library/configparser.html#module-configparser).**