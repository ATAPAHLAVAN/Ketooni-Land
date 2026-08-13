"""
جایگزین کن با: products/views.py
فیلتر، مرتب‌سازی، محصولات مشابه اضافه شده.
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category


def _apply_filters_and_sort(request, products):
    # فیلتر برند/دسته‌بندی از querystring (چندتایی)
    brands = request.GET.getlist('brand')
    if brands:
        products = products.filter(category__slug__in=brands)

    # فیلتر رنگ
    colors = request.GET.getlist('color')
    if colors:
        products = products.filter(color__in=colors)

    # فیلتر سایز
    sizes = request.GET.getlist('size')
    if sizes:
        products = products.filter(sizes__size__in=sizes).distinct()

    # فیلتر قیمت
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # مرتب‌سازی
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    return products


def product_list(request):
    products = Product.objects.filter(is_active=True)
    products = _apply_filters_and_sort(request, products)

    paginator = Paginator(products, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'total_count': products.count(),
        'categories': Category.objects.filter(is_active=True),
        'colors': Product.COLOR_CHOICES,
        'current_sort': request.GET.get('sort', 'newest'),
        'selected_brands': request.GET.getlist('brand'),
        'selected_colors': request.GET.getlist('color'),
        'selected_sizes': request.GET.getlist('size'),
    }
    return render(request, 'products/product_list.html', context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    products = _apply_filters_and_sort(request, products)

    paginator = Paginator(products, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'category': category,
        'products': page_obj,
        'page_obj': page_obj,
        'total_count': products.count(),
        'categories': Category.objects.filter(is_active=True),
        'colors': Product.COLOR_CHOICES,
        'current_sort': request.GET.get('sort', 'newest'),
        'selected_brands': request.GET.getlist('brand'),
        'selected_colors': request.GET.getlist('color'),
        'selected_sizes': request.GET.getlist('size'),
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # محصولات مشابه: همون دسته‌بندی، بجز خودش
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    from reviews.models import Review
    reviews = Review.objects.filter(product=product, is_approved=True).order_by('-created_at')

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'average_rating': product.get_average_rating(),
        'review_count': product.get_review_count(),
    }
    return render(request, 'products/product_detail.html', context)


def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    products = _apply_filters_and_sort(request, products)

    paginator = Paginator(products, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'query': query,
        'total_count': products.count(),
        'categories': Category.objects.filter(is_active=True),
        'colors': Product.COLOR_CHOICES,
        'current_sort': request.GET.get('sort', 'newest'),
    }
    return render(request, 'products/product_list.html', context)
def live_search(request):
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_active=True
    )[:6]
    
    results = []
    for product in products:
        results.append({
            'name': product.name,
            'price': int(product.get_price()),
            'image_url': product.image.url if product.image else '',
            'url': f'/shoes/product/{product.slug}/',
            'category': product.category.name,
        })
    
    return JsonResponse({'results': results})