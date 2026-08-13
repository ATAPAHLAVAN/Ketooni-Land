from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import Cart, CartItem



@login_required
def create_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    if not items.exists():
        return redirect('cart:view_cart')


    
    subtotal = cart.get_total()
    discount_percent = request.session.get('discount_percent', 0)
    discount_amount = subtotal * discount_percent / 100 if discount_percent else 0
    total = subtotal - discount_amount

    

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # ساخت سفارش
        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            phone=phone,
            address=address,
            total_price=total,
            status='pending',
        )

        # انتقال آیتم‌های سبد خرید به سفارش
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                size=item.size,
                quantity=item.quantity,
                price=item.product.get_price(),
            )

        # خالی کردن سبد خرید بعد از ثبت سفارش
        items.delete()
        request.session.pop('discount_percent', None)
        request.session.pop('discount_code', None)

        return redirect('payment:payment_page', order_id=order.id)
    
    context = {
        'items': items,
        'cart_total': total,
    }
    return render(request, 'orders/create_order.html', context)

    

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()

    return redirect('orders:order_detail', order_id=order.id)


@login_required
def download_invoice(request, order_id):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm

    order = get_object_or_404(Order, id=order_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice-{order.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 40 * mm
    p.setFont("Helvetica-Bold", 18)
    p.drawString(20 * mm, y, f"Invoice #{order.id}")

    y -= 15 * mm
    p.setFont("Helvetica", 11)
    p.drawString(20 * mm, y, f"Customer: {order.customer_name}")
    y -= 7 * mm
    p.drawString(20 * mm, y, f"Phone: {order.phone}")
    y -= 7 * mm
    p.drawString(20 * mm, y, f"Address: {order.address}")
    y -= 7 * mm
    p.drawString(20 * mm, y, f"Status: {order.status}")
    y -= 7 * mm
    p.drawString(20 * mm, y, f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}")

    y -= 15 * mm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(20 * mm, y, "Items:")
    y -= 8 * mm

    p.setFont("Helvetica", 10)
    for item in order.items.all():
        line = f"{item.product.name}  x{item.quantity}  -  {item.price} Toman"
        p.drawString(25 * mm, y, line)
        y -= 6 * mm

    y -= 10 * mm
    p.setFont("Helvetica-Bold", 13)
    p.drawString(20 * mm, y, f"Total: {order.total_price} Toman")

    p.showPage()
    p.save()
    return response

    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()

    return redirect('orders:order_list')