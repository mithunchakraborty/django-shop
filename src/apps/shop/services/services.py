from ..models import Category, Product
from django.shortcuts import render, get_object_or_404


def get_all_categories():
    """
    Gets all kinds of categories from the database.
    """
    return Category.objects.all() 


def get_available_products():
    """
    Retrieves only available products from the database.
    """
    return Product.objects.filter(available=True)


def get_category_with_slug(category_slug):
    """
    Gets a category with slug from the database.
    """
    return get_object_or_404(Category, slug=category_slug)


def get_product(id, slug):
    """
    Gets a product from the database.
    """
    return get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True
    )

