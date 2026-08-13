"""
جایگزین کن با: cart/views.py
کد تخفیف اضافه شده (ذخیره در session).
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product, DiscountCode
from cart.models import Cart, CartItem


@login_required(login_url='accounts:login')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    subtotal = cart.get_total()

    discount_percent = request.session.get('discount_percent', 0)
    discount_code = request.session.get('discount_code', '')
    discount_amount = subtotal * discount_percent / 100 if discount_percent else 0
    total = subtotal - discount_amount

    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'discount_percent': discount_percent,
        'discount_code': discount_code,
        'discount_amount': discount_amount,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='accounts:login')
@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    size = request.POST.get('size', '')
    quantity = int(request.POST.get('quantity', 1))

    try:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        if size and product.sizes.exists():
            size_obj = product.sizes.filter(size=size).first()
            if not size_obj or size_obj.stock < quantity:
                return JsonResponse({'success': False, 'message': 'موجودی کافی نیست'})

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, product=product, size=size,
            defaults={'quantity': quantity}
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({
            'success': True,
            'message': 'محصول اضافه شد!',
            'cart_count': cart.items.count(),
            'total': float(cart.get_total())
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required(login_url='accounts:login')
@require_POST
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect('cart:view_cart')


@login_required(login_url='accounts:login')
@require_POST
def update_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()

    return redirect('cart:view_cart')


@login_required(login_url='accounts:login')
@require_POST
def apply_discount(request):
    code = request.POST.get('code', '').strip()

    try:
        discount = DiscountCode.objects.get(code__iexact=code)
        if discount.is_valid():
            request.session['discount_percent'] = discount.percent
            request.session['discount_code'] = discount.code
            messages_text = f'کد تخفیف {discount.percent}% با موفقیت اعمال شد'
            success = True
        else:
            messages_text = 'این کد تخفیف منقضی شده یا معتبر نیست'
            success = False
    except DiscountCode.DoesNotExist:
        messages_text = 'کد تخفیف نامعتبر است'
        success = False

    from django.contrib import messages
    if success:
        messages.success(request, messages_text)
    else:
        messages.error(request, messages_text)

    return redirect('cart:view_cart')


@login_required(login_url='accounts:login')
def remove_discount(request):
    request.session.pop('discount_percent', None)
    request.session.pop('discount_code', None)
    return redirect('cart:view_cart')