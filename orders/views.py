from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from products.models import Product
import random
import string

def get_or_create_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']

def cart_detail(request):
    cart = get_or_create_cart(request)
    items = []
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass
    return render(request, 'orders/cart.html', {'items': items, 'total': total})

def add_to_cart(request, product_id):
    cart = get_or_create_cart(request)
    product_id = str(product_id)
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session.modified = True
    messages.success(request, 'Item added to cart!')
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = get_or_create_cart(request)
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session.modified = True
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart:
        return redirect('cart_detail')
    items = []
    subtotal = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = product.price * quantity
            subtotal += item_total
            items.append({'product': product, 'quantity': quantity, 'subtotal': item_total})
        except Product.DoesNotExist:
            pass
    if request.method == 'POST':
        otp = ''.join(random.choices(string.digits, k=6))
        order = Order.objects.create(
            customer=request.user,
            delivery_address=request.POST.get('address'),
            delivery_city=request.POST.get('city'),
            delivery_state=request.POST.get('state'),
            delivery_phone=request.POST.get('phone'),
            subtotal=subtotal,
            total=subtotal,
            delivery_otp=otp,
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price,
            )
        request.session['cart'] = {}
        request.session['pending_order_id'] = order.id
        return redirect('initiate_payment', order_id=order.id)
    return render(request, 'orders/checkout.html', {'items': items, 'subtotal': subtotal})

@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def confirm_delivery(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == order.delivery_otp:
            order.otp_verified = True
            order.status = 'delivered'
            order.save()
            messages.success(request, 'Delivery confirmed! Thank you.')
        else:
            messages.error(request, 'Invalid OTP. Please check and try again.')
    return redirect('order_detail', order_id=order.id)
