from django.db import models
from accounts.models import CustomUser
from orders.models import Order

class Dispute(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('under_review', 'Under Review'),
        ('resolved_buyer', 'Resolved - Buyer Favour'),
        ('resolved_seller', 'Resolved - Seller Favour'),
        ('closed', 'Closed'),
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    raised_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    evidence = models.FileField(upload_to='dispute_evidence/', blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='open')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Dispute on Order #{self.order.id}"
