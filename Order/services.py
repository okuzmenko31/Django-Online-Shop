import secrets
from Coupons.models import Coupons


def generate_code():
    """This function generates some numbers"""
    return secrets.token_hex(3)


def get_product_cost(price, quantity):
    """Here we are returning the calculated value of the total cost, by multiplying the product price
     for its quantity"""
    return float(price * quantity)
