from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order


@login_required
def confirm_delivery(request, order_id):
    """
    Placeholder for courier webhook or manual delivery confirmation.
    In production, integrate Sendbox/GIG webhook here.
    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = 'shipped'
        order.save()
        messages.success(request, f'Order #{order.id} marked as shipped.')
    return redirect('dashboard:order_detail', order_id=order.id)
