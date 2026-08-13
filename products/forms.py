from django import forms
from .models import Product, Category

class ProductFilterForm(forms.Form):
    """فرم فیلتر محصول‌ها"""
    
    SORT_CHOICES = [
        ('-created_at', 'جدیدترین'),
        ('price', 'قیمت: کم به زیاد'),
        ('-price', 'قیمت: زیاد به کم'),
        ('name', 'نام: A-Z'),
        ('-rating', 'بهترین امتیاز'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو کفش...',
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='دسته‌بندی'
    )
    
    brand = forms.ChoiceField(
        choices=[('', 'تمام برندها')] + Product.BRAND_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='برند'
    )
    
    min_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'کمترین قیمت',
        }),
        label='کمترین قیمت'
    )
    
    max_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'بیشترین قیمت',
        }),
        label='بیشترین قیمت'
    )
    
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
        label='مرتب‌سازی'
    )


class ProductReviewForm(forms.Form):
    """فرم نوشتن نظر برای محصول"""
    
    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ فوق‌العاده'),
        (4, '⭐⭐⭐⭐ خیلی خوب'),
        (3, '⭐⭐⭐ خوب'),
        (2, '⭐⭐ متوسط'),
        (1, '⭐ ضعیف'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        }),
        label='امتیاز'
    )
    
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان نظر',
        }),
        label='عنوان'
    )
    
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'نظرتان را بنویسید...',
            'rows': 5,
        }),
        label='متن نظر'
    )
    
    is_verified_purchase = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='خرید تایید شده'
    )