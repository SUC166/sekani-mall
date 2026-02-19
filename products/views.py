from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def product_list(request):
    products = Product.objects.filter(status='active').order_by('-created_at')
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    condition = request.GET.get('condition', '')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if condition:
        products = products.filter(condition=condition)

    featured = Product.objects.filter(status='active', is_featured=True)[:6]
    context = {
        'products': products,
        'categories': categories,
        'featured': featured,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, status='active')
    related = Product.objects.filter(category=product.category, status='active').exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {'product': product, 'related': related})
