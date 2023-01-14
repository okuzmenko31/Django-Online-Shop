def get_discount(price, discount):
    """Calculating discount"""

    discount = float(price * discount / 100)
    total = float(price - discount)
    int_total = int(total)
    return int_total  # returning price with discount


def get_price_sep(price):
    """Here we are getting product price, but in string representation to put a space
     separator for a nicer look of price value for user"""

    product_price = str(price)

    if len(product_price) == 4:

        first_part_price = product_price[:1]
        second_part_price = product_price[1:]
        total = " ".join([first_part_price, second_part_price])

        return total

    elif len(product_price) == 5:

        first_part_price = product_price[:2]
        second_part_price = product_price[2:]
        total = " ".join([first_part_price, second_part_price])

        return total

    elif len(product_price) == 6:

        first_part_price = product_price[:3]
        second_part_price = product_price[3:]
        total = " ".join([first_part_price, second_part_price])

        return total

    elif len(product_price) == 7:

        first_part_price = product_price[0]
        second_part_price = product_price[1:4]
        third_part_price = product_price[4:]

        total = " ".join([first_part_price, second_part_price, third_part_price])

        return total

    else:
        return price


def get_rating_star(rating):
    if 5.1 > rating > 4.9:
        return '<img src="/static/stars/star.png">' * 5
    elif 4.8 > rating > 4.4:
        return '<img src="/static/stars/star.png">' * 4 + '<img src="/static/stars/rating.png">'
    elif 4.5 > rating > 3.9:
        return '<img src="/static/stars/star.png">' * 4 + '<img src="/static/stars/empty_star.png">'
    elif 3.9 > rating > 3.4:
        return '<img src="/static/stars/star.png">' * 3 + '<img src="/static/stars/rating.png">' + \
               '<img src="/static/stars/empty_star.png">'
    elif 3.5 > rating > 2.9:
        return '<img src="/static/stars/star.png">' * 3 + '<img src="/static/stars/empty_star.png">' * 2
    elif 2.8 > rating > 2.4:
        return '<img src="/static/stars/star.png">' * 2 + '<img src="/static/stars/rating.png">' + \
               '<img src="/static/stars/empty_star.png">' * 2
    elif 2.5 > rating > 1.9:
        return '<img src="/static/stars/star.png">' * 2 + '<img src="/static/stars/empty_star.png">' * 3
    elif 1.8 > rating > 1.4:
        return '<img src="/static/stars/star.png">' * 1 + '<img src="/static/stars/rating.png">' + \
               '<img src="/static/stars/empty_star.png">' * 3
    elif 1.5 > rating > 0.9:
        return '<img src="/static/stars/star.png">' * 1 + '<img src="/static/stars/empty_star.png">' * 4
    else:
        return '<img src="/static/stars/empty_star.png">' * 5
