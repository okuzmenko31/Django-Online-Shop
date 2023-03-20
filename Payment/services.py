import random
from Coupons.models import Coupons
from Products.models import ProductSubcategory


def create_coupon(user):
    """This function creates user's coupon."""
    subcategories = ProductSubcategory.objects.all()
    subs = []

    for subcategory in subcategories:
        subs.append(subcategory)
    sub = random.choice(subs)  # a random subcategory is selected

    if not Coupons.objects.filter(user=user, subcategory=sub, is_active=True).exists():
        Coupons.objects.create(user=user,
                               subcategory=sub,
                               discount=random.randint(1, 20))
