from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from wishlist.models import Wishlist

@login_required(login_url='accounts:login')
def view_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    
    context = {
        'wishlist': wishlist,
        'products': products,
    }
    return render(request, 'wishlist/wishlist.html', context)

@login_required(login_url='accounts:login')
@require_POST
def add_to_wishlist(request):
    """AJAX: اضافه کردن به علاقه‌مندی"""
    product_id = request.POST.get('product_id')
    
    try:
        product = get_object_or_404(Product, id=product_id)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        if wishlist.products.filter(id=product_id).exists():
            wishlist.products.remove(product)
            return JsonResponse({
                'success': True,
                'message': 'از علاقه‌مندی حذف شد',
                'is_wishlisted': False
            })
        else:
            wishlist.products.add(product)
            return JsonResponse({
                'success': True,
                'message': 'به علاقه‌مندی اضافه شد!',
                'is_wishlisted': True
            })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required(login_url='accounts:login')
@require_POST
def remove_from_wishlist(request, product_id):
    """حذف از علاقه‌مندی"""
    wishlist = get_object_or_404(Wishlist, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.remove(product)
    
    return redirect('wishlist:view_wishlist')