"""
جایگزین کن با: products/models.py
این نسخه فیلد رنگ و تخفیف رو هم اضافه کرده.
اگه از قبل ProductSize و بقیه رو داری نگه‌شون دار، فقط موارد جدید رو اضافه کن.
"""

from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    COLOR_CHOICES = [
        ('black', 'مشکی'),
        ('white', 'سفید'),
        ('red', 'قرمز'),
        ('blue', 'آبی'),
        ('gray', 'طوسی'),
        ('green', 'سبز'),
        ('multi', 'چندرنگ'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, validators=[MinValueValidator(0)])
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='black')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_price(self):
        return self.discount_price if self.discount_price else self.price

    def get_average_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(product=self, is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    def get_review_count(self):
        from reviews.models import Review
        return Review.objects.filter(product=self, is_approved=True).count()


class ProductSize(models.Model):
    SIZES = [(str(s), str(s)) for s in range(35, 47)]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=10, choices=SIZES)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.name} - Size {self.size}"


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percent = models.PositiveIntegerField(help_text="درصد تخفیف، مثلا 10 برای 10%")
    max_uses = models.PositiveIntegerField(default=100)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.percent}%)"

    def is_valid(self):
        from django.utils import timezone
        if not self.is_active:
            return False
        if self.used_count >= self.max_uses:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return True