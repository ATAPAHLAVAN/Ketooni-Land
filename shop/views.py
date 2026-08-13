from django.shortcuts import render
from products.models import Category, Product

def index(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'shop/index.html', context)

def about(request):
    return render(request, 'shop/about.html')