import requests
import json
import hmac
import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from orders.models import Order

FLUTTERWAVE_SECRET = settings.FLUTTERWAVE_SECRET_KEY
FLW_BASE = settings.FLUTTERWAVE_BASE_URL

@login_required
def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    tx_ref = f"SEKANI-{order.id}-{request.user.id}"
    order.flutterwave_tx_ref = tx_ref
    order.save()

    payload = {
        "tx_ref": tx_ref,
        "amount": str(order.total),
        "currency": "NGN",
        "redirect_url": request.build_absolute_uri(f"/payments/verify/{order.id}/"),
        "customer": {
            "email": request.user.email,
            "phonenumber": request.user.phone,
            "name": request.user.get_full_name(),
        },
        "customizations": {
            "title": "SEKANI Mall",
            "description": f"Payment for Order #{order.id}",
            "logo": request.build_absolute_uri('/static/images/logo.png'),
        },
        "meta": {
            "order_id": order.id,
        }
    }

    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET}",
        "Content-Type": "application/json",
    }

    response = requests.post(f"{FLW_BASE}/payments", json=payload, headers=headers)
    data = response.json()

    if data.get('status') == 'success':
        payment_link = data['data']['link']
        return redirect(payment_link)
    else:
        return render(request, 'payments/payment_error.html', {'order': order})

@login_required
def verify_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    tx_id = request.GET.get('transaction_id')
    status = request.GET.get('status')

    if status != 'successful' or not tx_id:
        order.status = 'cancelled'
        order.save()
        return render(request, 'payments/payment_failed.html', {'order': order})

    headers = {"Authorization": f"Bearer {FLUTTERWAVE_SECRET}"}
    response = requests.get(f"{FLW_BASE}/transactions/{tx_id}/verify", headers=headers)
    data = response.json()

    if (data.get('status') == 'success' and
        data['data']['status'] == 'successful' and
        data['data']['tx_ref'] == order.flutterwave_tx_ref and
        float(data['data']['amount']) >= float(order.total)):

        order.status = 'paid'
        order.flutterwave_tx_id = tx_id
        order.save()

        # Reduce stock
        for item in order.items.all():
            item.product.stock -= item.quantity
            item.product.save()

        return render(request, 'payments/payment_success.html', {'order': order})
    else:
        order.status = 'cancelled'
        order.save()
        return render(request, 'payments/payment_failed.html', {'order': order})

@csrf_exempt
def flutterwave_webhook(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    secret_hash = settings.FLUTTERWAVE_SECRET_KEY
    signature = request.headers.get('verif-hash')
    if signature != secret_hash:
        return HttpResponse(status=401)

    payload = json.loads(request.body)
    event = payload.get('event')

    if event == 'charge.completed':
        tx_ref = payload['data']['tx_ref']
        try:
            order = Order.objects.get(flutterwave_tx_ref=tx_ref)
            if payload['data']['status'] == 'successful':
                order.status = 'paid'
                order.save()
        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)

@login_required
def release_escrow(request, order_id):
    """SEKANI admin manually releases escrow after delivery confirmed"""
    if not request.user.is_sekani_admin():
        return HttpResponse(status=403)
    order = get_object_or_404(Order, id=order_id)
    if order.otp_verified and not order.escrow_released:
        order.escrow_released = True
        order.save()
    return redirect('dashboard_orders')
