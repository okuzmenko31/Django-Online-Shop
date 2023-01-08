from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Reviews, Product, ProductMemoryChoice, ProductVersionChoice, ProductColorChoice


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


@receiver(post_save, sender=Product)
def get_memory_choice(**kwargs):
    instance = kwargs['instance']

    if instance.product_memory:
        ProductMemoryChoice.objects.create(product=instance, category=instance.subcategory,
                                           color=instance.product_color,
                                           version=instance.product_version, memory=instance.product_memory.memory_size
                                           )


@receiver(post_save, sender=Product)
def get_version_choice(**kwargs):
    instance = kwargs['instance']

    if instance.product_version:
        ProductVersionChoice.objects.create(product=instance, category=instance.subcategory,
                                            memory=instance.product_memory,
                                            color=instance.product_color, version=instance.product_version.title)


@receiver(post_save, sender=Product)
def get_color_choice(**kwargs):
    instance = kwargs['instance']

    if instance.product_color:
        ProductColorChoice.objects.create(product=instance, category=instance.subcategory,
                                          color=instance.product_color.color, memory=instance.product_memory,
                                          version=instance.product_version, is_active=True,
                                          background_color=instance.product_color.color_hex)
