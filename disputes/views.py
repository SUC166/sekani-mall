from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dispute
from orders.models import Order

@login_required
def raise_dispute(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if request.method == 'POST':
        Dispute.objects.get_or_create(
            order=order,
            defaults={
                'raised_by': request.user,
                'reason': request.POST.get('reason'),
                'evidence': request.FILES.get('evidence'),
            }
        )
        order.status = 'disputed'
        order.save()
        messages.success(request, 'Dispute raised. SEKANI team will review within 24 hours.')
        return redirect('order_detail', order_id=order.id)
    return render(request, 'disputes/raise_dispute.html', {'order': order})
