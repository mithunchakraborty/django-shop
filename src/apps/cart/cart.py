from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart(object):
    """
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

        # Save the currently applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def add_or_update_cart_item(
        self,
        product,
        quantity=1,
        update_quantity=False
    ) -> None:
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save_cart_state()

    def save_cart_state(self) -> None:
        """
        Save cart state.
        """
        # Update cart session
        self.session[settings.CART_SESSION_ID] = self.cart

        # Mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove_item_from_cart(self, product) -> None:
        """
        Remove item from cart.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save_cart_state()

    def __iter__(self):
        """
        Looping through the items in the cart and getting 
        products from the database.
        """
        product_ids = self.cart.keys()

        # Getting product objects and adding them to cart
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Counting all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_cost(self):
        """
        Calculation of the cost of goods in the basket.
        """
        return sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values()
        )

    def clean_cart(self) -> None:
        """
        Emptying the trash session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def coupon(self):
        """
        """
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)

        return None

    def get_discount(self):
        """
        If the cart contains a coupon, receive a rate discount
        and refund the amount that will be deducted 
        from the total amount of the cart.
        """
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) \
                * self.get_total_cost()

        return Decimal('0')

    def get_total_price_after_discount(self):
        """
        Returns the total amount of the cart after subtracting 
        the amount returned by the get_discount () method.
        """
        return self.get_total_cost() - self.get_discount()

