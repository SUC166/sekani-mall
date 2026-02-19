from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    CONDITION_CHOICES = (
        ('new', 'New'),
        ('fairly_used', 'Fairly Used'),
    )
    TYPE_CHOICES = (
        ('physical', 'Physical'),
        ('digital', 'Digital'),
        ('service', 'Service'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('out_of_stock', 'Out of Stock'),
        ('archived', 'Archived'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    product_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='physical')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    stock = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=False)
    digital_file = models.FileField(upload_to='digital_products/', blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0 and self.status == 'active'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"
