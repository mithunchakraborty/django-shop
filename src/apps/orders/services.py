from django.core.mail import send_mail
from .models import Order


def send_email_if_order_created(order_id):
    """
    Task to send an email notification when an order has been successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order_id}'
    message = f"""
        Dear {order.first_name},\n\n
        You have successfully placed an order.
        Your order id is {order.id}.
    """

    send_mail(
        subject,
        message,
        'den.armstrong99@gmail.com',
        [order.email]
    )


