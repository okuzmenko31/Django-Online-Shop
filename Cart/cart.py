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
            """If our cart not in the session, 
            we creating it in the session"""
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def save(self):
        """When we are calling this method, we are saving our cart in the session"""
        self.session[settings.CART_SESSION_ID] = self.cart
        # Mark a session as "modified" to make sure it's saved
        self.session.modified = True

    def add(self, product):
        """Method for adding product to the cart"""
        product_id = str(product.id)

        if product_id not in self.cart:
            """If product not in the cart, we adding it"""
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price_with_discount),
                                     'price_usd': str(product.price_in_usd_with_discount)}

        self.cart[product_id]['quantity'] += 1  # every adding product to the cart its quantity increasing by 1
        self.save()

    def remove(self, product):
        """Method of removing product from the cart"""
        product_id = str(product.id)

        if product_id in self.cart:
            """If product in the cart, it will be removed"""
            del self.cart[product_id]
            self.save()

    def add_quantity(self, product):
        """Method of increasing product quantity in the cart"""
        product_id = str(product.id)

        if product_id in self.cart:
            """If product is in the cart, his quantity will increase by 1"""
            self.cart[product_id]['quantity'] += 1
            self.save()

    def minus_quantity(self, product):
        """Method of decreasing product quantity in the cart"""
        product_id = str(product.id)

        if product_id in self.cart:
            """If product is in the cart, his quantity will decrease by 1"""
            if self.cart[product_id]['quantity'] > 0:
                self.cart[product_id]['quantity'] -= 1
            else:
                self.remove(product)
            self.save()

    def __iter__(self):
        """Iterating through items in the basket and getting the products from the database.
        Adding to the basket the objects of the model."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids).select_related('main_category',
                                                                             'subcategory')
        # getting all products, whose IDs in the cart

        for product in products:
            """In every id of product in the cart assigns value 'product',
            and a queryset of filtered products is assigned in the 'product'."""
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            """Here we are iterating through values in the cart and
            override old values or create new value."""
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['price_usd'] = Decimal(item['price_usd'])
            item['total_price_usd'] = item['price_usd'] * item['quantity']
            item['total_price_view'] = get_price_sep(item['total_price'])  # total price of product for template
            item['total_price_usd_view'] = get_price_sep(
                item['total_price_usd'])  # total price of product in usd for template
            item['price_view'] = get_price_sep(item['price'])  # product price for template
            item['price_usd_view'] = get_price_sep(item['price_usd'])  # product price in usd for template
            yield item

    def __len__(self):
        """Counting all products in the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Getting overall total price of all products in the cart"""
        return sum(item['price'] * item['quantity'] for item in self.cart.values())

    def get_total_price_for_template(self):
        """Getting overall total price of all products in the CART, but separated.
        Look at the services.py in the Products directory to see how it works."""
        return get_price_sep(self.get_total_price())

    def get_total_price_usd(self):
        """Getting overall total price of all products in the cart but in dollars"""
        return sum(item['price_usd'] * item['quantity'] for item in self.cart.values())

    def get_total_price_usd_for_template(self):
        """Getting overall total price of all products in the CART, but separated.
        Look at the services.py in the Products directory to see how it works. But in dollars"""
        return get_price_sep(self.get_total_price_usd())

    def clear(self):
        """Removing cart from the session"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
