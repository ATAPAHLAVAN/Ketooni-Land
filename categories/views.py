from django.shortcuts import render
from products.models import Category

def categories_list(request):
    categories = Category.objects.filter(is_active=True)
    context = {
        'categories': categories,
    }
    return render(request, 'categories/list.html', context)