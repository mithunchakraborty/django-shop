import logging
from django.shortcuts import render
from core.views import base_view, BaseView
from .services.services import *


logger = logging.getLogger(__name__)


# @base_view
def get_product_list_view(request, category_slug=None):
    """
    Receiving a list of goods.
    """
    category = None
    categories = get_all_categories()

    products = get_available_products()

    if category_slug:
        category = get_category_with_slug(category_slug)
        products = products.filter(category=category)

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
    product = get_product(id, slug)

    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product
        }
    )

