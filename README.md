## Python + Django project of web store

- **python 3.11**
- **Django 4.1.3**
- **postgres 15**

## Clone Repository

```
https://github.com/okuzmenko31/Django-Online-Shop.git
```

## Go to project directory

```
cd Django-Online-Shop
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

## Change DB connection in settings.py

### Change DATABASE settings in settings.py to following:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shop_db',
        'USER': 'shop_user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': 5432
    }
}
```

## Running docker-container

- **Run the Docker desktop ([Install](https://docs.docker.com/get-docker/) if you don't have it)**
- **Go to docker-compose.yml and in service db
  change environment settings to the following:**

```
    environment:
      POSTGRES_USER: shop_user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: shop_db
```

- **Build docker container and run it**

```
docker-compose build
docker-compose up -d
```

## Make migrations and migrate them to the database

```
docker-compose run shop-app python manage.py makemigrations
docker-compose run shop-app python manage.py migrate
```

## Create superuser

```
docker-compose run shop-app python manage.py createsuperuser
```

## Connection to gmail

## In settings.py replace gmail settings to following:

```
EMAIL_HOST = smtp.gmail.com
EMAIL_HOST_USER = your_gmail
EMAIL_HOST_PASSWORD = your_password
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

- **Change the content of EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
  to yours gmail and password from it.**


- **For more information about connection to gmail, [click here.](https://support.google.com/mail/answer/7126229?hl=en)** 
