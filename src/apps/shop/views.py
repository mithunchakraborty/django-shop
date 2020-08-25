import logging
from django.shortcuts import render
from core.views import base_view, BaseView
from .services.services import *
from cart.forms import CartAddProductForm


logger = logging.getLogger(__name__)


# @base_view
def get_product_list_view(request, category_slug=None):
    """
    Receiving a list of goods.
    """
    category = None
    categories = get_all_categories()

    products = get_available_products()

    try:
        if category_slug:
            category = get_category_with_slug(category_slug)
            products = products.filter(category=category)
    except Exception as ex:
        logger.error(
            f"""
            [get_product_list_view] No category_slug matches 
            the given query
            """
        )

    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products
        }
    )


# @base_view
def get_product_detail_view(request, id, slug):
    """
    Receiving one item.
    """
    try: 
        product = get_product(id, slug)
    except Exception as ex:
        logger.error(
            f"""
            [get_product_detail_view] No Product matches the 
            given query with id = {id} and slug = {slug}
            """
        )

    cart_product_form = CartAddProductForm()

    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
            'cart_product_form': cart_product_form
        }
    )

