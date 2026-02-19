from django.db import models
from accounts.models import CustomUser
from products.models import Product
from discounts.models import Discount

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('paid', 'Paid - Awaiting Shipment'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('disputed', 'Disputed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_address = models.TextField()
    delivery_city = models.CharField(max_length=100)
    delivery_state = models.CharField(max_length=100)
    delivery_phone = models.CharField(max_length=20)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_otp = models.CharField(max_length=6, blank=True)
    otp_verified = models.BooleanField(default=False)
    flutterwave_tx_ref = models.CharField(max_length=200, blank=True)
    flutterwave_tx_id = models.CharField(max_length=200, blank=True)
    escrow_released = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def get_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
