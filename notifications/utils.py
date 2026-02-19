from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation_email(order):
    subject = f'SEKANI Mall - Order #{order.id} Confirmed!'
    message = f"""
Hi {order.customer.first_name},

Your order #{order.id} has been confirmed and payment received!

Order Total: ₦{order.total}
Delivery Address: {order.delivery_address}, {order.delivery_city}, {order.delivery_state}

We will notify you once your order is shipped.

Thank you for shopping with SEKANI Mall!
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.customer.email], fail_silently=True)


def send_otp_email(order):
    subject = f'SEKANI Mall - Delivery OTP for Order #{order.id}'
    message = f"""
Hi {order.customer.first_name},

Your delivery OTP for Order #{order.id} is:

    {order.otp}

Please share this OTP with the delivery agent ONLY when you have received your package in good condition.

DO NOT share this OTP before receiving your order.

SEKANI Mall Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.customer.email], fail_silently=True)


def send_status_update_email(order):
    subject = f'SEKANI Mall - Order #{order.id} Update'
    message = f"""
Hi {order.customer.first_name},

Your Order #{order.id} status has been updated to: {order.get_status_display().upper()}

Track your order at: https://sekanimal.com/orders/{order.id}/

SEKANI Mall Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.customer.email], fail_silently=True)
