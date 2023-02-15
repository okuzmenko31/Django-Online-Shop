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

## Running docker-container

- **Run the Docker ([Install](https://docs.docker.com/get-docker/) if you don't have it)**
- **Go to docker-compose.yml and in service rvshop_db
  change environment settings to the following:**

```
    environment:
      POSTGRES_USER: rvshop_user
      POSTGRES_PASSWORD: rvshop_password
      POSTGRES_DB: rvshop_database
```

- **Build docker container and run it**

```
docker-compose build
docker-compose up -d
```

## Change DB connection in settings.py

### Comment all DATABASE settings in settings.py and paste this database settings:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rvshop_database',
        'USER': 'rvshop_user',
        'PASSWORD': 'rvshop_password',
        'HOST': 'rvshop_db',
        'PORT': 5432
    }
}
```

## Make migrations and migrate them to the database

```
docker-compose run rvshop-web-app python manage.py makemigrations
docker-compose run rvshop-web-app python manage.py migrate
```

## Create superuser

```
docker-compose run rvshop-web-app python manage.py createsuperuser
```

## About email connection in settings.py

- **For correct work of sending letters, you need to replace
  available email to yours and write you password instead of
  available. I used connection with gmail.com, if you want to
  connect with it [click here](https://support.google.com/mail/answer/7126229?hl=ru)
  for more information about it.**
- **Also, my gmail password was hidden with ConfigParser, you can
  read the documentation [here](https://docs.python.org/3/library/configparser.html#module-configparser).**