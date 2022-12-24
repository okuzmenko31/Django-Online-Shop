from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Reviews


@receiver(post_save, sender=Reviews)
def get_total_rating(**kwargs):
    instance = kwargs['instance']

    product = instance.product

    reviews = Reviews.objects.filter(product=product)

    count_of_rating = 0

    for item in reviews:
        count_of_rating += item.rating
        product.total_rating = count_of_rating / len(reviews.values())

    instance.product.save()
