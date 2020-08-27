from django.core.mail import send_mail
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


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
            send_mail(
                'Subject here',
                'Here is the message.',
                'motyletsdenis@gmail.com',
                ['den.armstrong99@gmail.com'],
                fail_silently=False,
                    
            )
            
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

