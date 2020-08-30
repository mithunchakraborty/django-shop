from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.services.services import get_product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def add_product_to_cart(request, product_id):
    """
    Adds a product to the cart. Returns a view of the cart.
    """
    cart = Cart(request)
    product = get_product(id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add_or_update_cart_item(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )

    return redirect('cart:cart_detail')


def remove_product_from_cart(request, product_id):
    """
    Removes an item from the cart. Returns a view of the cart.
    """
    cart = Cart(request)
    product = get_product(id=product_id)
    cart.remove_item_from_cart(product)

    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    Returns a view of the cart.
    """
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True}
        )

    coupon_apply_form = CouponApplyForm()

    return render(
        request, 
        'cart/detail.html', 
        {'cart': cart, 'coupon_apply_form': coupon_apply_form}
    )

