from django.db import models
from orders.models import Order


class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('escrowed', 'Escrowed'),
        ('released', 'Released'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    flutterwave_tx_ref = models.CharField(max_length=200, unique=True)
    flutterwave_tx_id = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    escrow_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.status}"
