from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Reviews, Product, ProductMemoryChoice, ProductVersionChoice, ProductColorChoice


@receiver(post_save, sender=Reviews)
def get_total_rating(**kwargs):
    """This signal is for getting total rating of product"""

    instance = kwargs['instance']
    product = instance.product
    reviews = Reviews.objects.filter(product=product)  # getting reviews which related with product

    count_of_rating = 0

    for item in reviews:
        count_of_rating += item.rating
        product.total_rating = count_of_rating / len(reviews.values())

    instance.product.save()


@receiver(post_save, sender=Product)
def get_product_choices(**kwargs):
    """This signal is for creating choices after adding a product"""

    instance = kwargs['instance']

    if not instance.editing:
        # instance.editing - this is boolean field which is needed to avoid
        # creation of similar choices of product after saving.

        if instance.product_memory:
            ProductMemoryChoice.objects.get_or_create(product=instance,
                                                      subcategory=instance.subcategory,
                                                      color=instance.product_color,
                                                      version=instance.product_version,
                                                      memory=instance.product_memory.memory_size
                                                      )

        if instance.product_version:
            ProductVersionChoice.objects.get_or_create(product=instance,
                                                       subcategory=instance.subcategory,
                                                       memory=instance.product_memory,
                                                       color=instance.product_color,
                                                       version=instance.product_version.title)

        if instance.product_color:
            ProductColorChoice.objects.get_or_create(product=instance,
                                                     subcategory=instance.subcategory,
                                                     color=instance.product_color.color,
                                                     memory=instance.product_memory,
                                                     version=instance.product_version,
                                                     is_active=True,
                                                     background_color=instance.product_color.color_hex)

        instance.editing = True  # value changing to True and similar choices won't be creating
        instance.save()
