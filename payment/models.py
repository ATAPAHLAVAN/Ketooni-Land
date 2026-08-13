from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('completed', 'موفق'),
        ('failed', 'ناموفق'),
        ('cancelled', 'لغو شده'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    authority = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - {self.status}"
    
    def is_paid(self):
        return self.status == 'completed'