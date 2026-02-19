from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from products.models import Product
from orders.models import Order

@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        order_id = request.POST.get('order_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        order = get_object_or_404(Order, id=order_id, customer=request.user, status='delivered')
        Review.objects.get_or_create(
            product=product,
            customer=request.user,
            order=order,
            defaults={'rating': rating, 'comment': comment}
        )
        messages.success(request, 'Thank you for your review!')
    return redirect('product_detail', slug=product.slug)
