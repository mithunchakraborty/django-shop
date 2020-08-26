from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def send_mail_about_order(order_id):
    """
    A task to send an email notification when 
    an order has been successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order_id}'
    message = f"""
        Dear {order.first_name},\n\n
        You have successfully placed an order.
        Your order id is {order.id}
    """
    
    return send_mail(
        subject,
        message,
        'admin@config.com',
        [order.email]
    )

