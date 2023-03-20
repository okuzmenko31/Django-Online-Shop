from .cart import Cart


def cart(request):
    """Context processor of cart."""

    return {'cart': Cart(request)}
