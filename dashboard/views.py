from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from products.models import Product, Category, ProductImage
from orders.models import Order
from disputes.models import Dispute
from discounts.models import Discount
from accounts.models import CustomUser

def sekani_admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_sekani_admin():
            return redirect('sekani_admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

@sekani_admin_required
def dashboard_home(request):
    context = {
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='paid').count(),
        'total_customers': CustomUser.objects.filter(role='customer').count(),
        'open_disputes': Dispute.objects.filter(status='open').count(),
        'recent_orders': Order.objects.order_by('-created_at')[:10],
    }
    return render(request, 'dashboard/home.html', context)

@sekani_admin_required
def dashboard_products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/products.html', {'products': products})

@sekani_admin_required
def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        product = Product.objects.create(
            name=name,
            slug=slugify(name),
            category_id=request.POST.get('category'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            condition=request.POST.get('condition'),
            product_type=request.POST.get('product_type'),
            stock=request.POST.get('stock'),
            is_featured=request.POST.get('is_featured') == 'on',
            created_by=request.user,
        )
        for image in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=image)
        messages.success(request, f'"{product.name}" added successfully!')
        return redirect('dashboard_products')
    return render(request, 'dashboard/add_product.html', {'categories': categories})

@sekani_admin_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.condition = request.POST.get('condition')
        product.stock = request.POST.get('stock')
        product.status = request.POST.get('status')
        product.is_featured = request.POST.get('is_featured') == 'on'
        product.save()
        for image in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=image)
        messages.success(request, 'Product updated!')
        return redirect('dashboard_products')
    return render(request, 'dashboard/edit_product.html', {'product': product, 'categories': categories})

@sekani_admin_required
def dashboard_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard/orders.html', {'orders': orders})

@sekani_admin_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()
        messages.success(request, f'Order #{order.id} status updated.')
    return redirect('dashboard_orders')

@sekani_admin_required
def dashboard_disputes(request):
    disputes = Dispute.objects.all().order_by('-created_at')
    return render(request, 'dashboard/disputes.html', {'disputes': disputes})

@sekani_admin_required
def dashboard_discounts(request):
    discounts = Discount.objects.all().order_by('-created_at')
    return render(request, 'dashboard/discounts.html', {'discounts': discounts})

@sekani_admin_required
def add_discount(request):
    if request.method == 'POST':
        Discount.objects.create(
            code=request.POST.get('code').upper(),
            discount_type=request.POST.get('discount_type'),
            value=request.POST.get('value'),
            minimum_order=request.POST.get('minimum_order', 0),
            max_uses=request.POST.get('max_uses', 100),
            valid_from=request.POST.get('valid_from'),
            valid_to=request.POST.get('valid_to'),
        )
        messages.success(request, 'Discount code created!')
        return redirect('dashboard_discounts')
    return render(request, 'dashboard/add_discount.html')
