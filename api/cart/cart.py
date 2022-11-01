from django.conf import settings

from decimal import Decimal

from shop import models

class Cart:
    """
    Cart system class.
    """

    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SETTINGS_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Add a product to the cart or change its quantity."""
        pass