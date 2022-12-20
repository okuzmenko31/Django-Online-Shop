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
        return "Занадто велика ціна до сплати, зменшіть кількість товарів"
