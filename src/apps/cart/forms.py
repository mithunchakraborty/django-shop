from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # Allows the user to select a quantity between 1-20
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int
    )

    """ 
    Allows you to specify whether to add an amount 
    to any existing value in the cart for a given 
    product (False) or if an existing value should 
    be updated with a given value (True) 
    """
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

