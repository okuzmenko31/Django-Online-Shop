from decimal import Decimal

from django.conf import settings

from Products.models import Product

from Products.services import get_price_sep


class Cart:

    def __init__(self, request):
        """Cart initializing"""

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # save an empty cart in the session

            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def save(self):
        # Updating session of cart

        self.session[settings.CART_SESSION_ID] = self.cart

        # Mark a session as "modified" to make sure it's saved
        self.session.modified = True

    def add(self, product):

        """
        Add product to the cart.
        """

        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price_with_discount),
                                     'price_usd': str(product.price_in_usd_with_discount)}

        self.cart[product_id]['quantity'] += 1
        self.save()

    def remove(self, product):
        """
        Removing product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def add_quantity(self, product):
        """Add quantity"""

        product_id = str(product.id)

        self.cart[product_id]['quantity'] += 1
        self.save()

    def minus_quantity(self, product):
        """Minus quantity"""

        product_id = str(product.id)

        self.cart[product_id]['quantity'] -= 1

        if self.cart[product_id]['quantity'] <= 0:
            self.remove(product)

        self.save()

    def __iter__(self):
        """
        Iterating through the items in the cart and getting the products from the database.
        """

        product_ids = self.cart.keys()
        # getting product objects and adding them to the cart
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['price_usd'] = Decimal(item['price_usd'])
            item['total_price_usd'] = item['price_usd'] * item['quantity']
            item['total_price_view'] = get_price_sep(item['total_price'])
            item['total_price_usd_view'] = get_price_sep(item['total_price_usd'])
            item['price_view'] = get_price_sep(item['price'])
            item['price_usd_view'] = get_price_sep(item['price_usd'])
            yield item

    def __len__(self):
        """
        Counting all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Counting the total price of products in cart
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_price_for_template(self):
        """
        Counting the total price of products in cart
        """
        summa = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

        products_total_price = get_price_sep(summa)

        return products_total_price

    def get_total_price_usd(self):
        """
        Counting the total price of products in cart
        """
        return sum(Decimal(item['price_usd']) * item['quantity'] for item in self.cart.values())

    def get_total_price_usd_for_template(self):
        """
        Counting the total price of products in cart
        """
        summa = sum(Decimal(item['price_usd']) * item['quantity'] for item in self.cart.values())

        products_total_price = get_price_sep(summa)

        return products_total_price

    def clear(self):
        # Removing cart from the session

        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
