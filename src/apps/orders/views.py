from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .services import send_email_if_order_created
from .models import Order
from django.contrib.admin.views.decorators import staff_member_required


def create_order_view(request):
    """
    """
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

            cart.clean_cart()

            # Send email
            send_email_if_order_created(order.id)
            
            return render(
                request,
                'orders/order/created.html',
                {'order': order}
            )

    else:
        form = OrderCreateForm

        return render(
            request,
            'orders/order/create.html',
            {'cart': cart, 'form': form}
        )


@staff_member_required
def admin_order_detail_view(request, order_id):
    """
    """
    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        'admin/orders/order/detail.html',
        {'order': order}
    )

