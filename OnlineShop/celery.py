import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineShop.settings')

app = Celery('OnlineShop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'update-product-price-every-2-days': {
        'task': 'Products.tasks.update_product_price_usd',
        'schedule': crontab(hour='*/48')
    }
}