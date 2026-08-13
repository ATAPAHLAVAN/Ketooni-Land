"""
جایگزین کن با: payment/views.py
نسخهٔ جدید API زرین‌پال (v4) - آدرس قدیمی حذف شده بود.
"""

import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from orders.models import Order
from .models import Payment

# ===== تنظیمات زرین‌پال (Sandbox / تستی - API v4) =====
MERCHANT_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"

# برای حالت واقعی (بعد از گرفتن Merchant ID واقعی)، این ۳ خط رو استفاده کن:
# ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
# ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
# ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/"


@login_required
def payment_page(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('shop:index')

    try:
        payment = Payment.objects.get(order=order)
    except Payment.DoesNotExist:
        payment = Payment.objects.create(
            user=request.user,
            order=order,
            amount=int(order.total_price)
        )

    context = {
        'order': order,
        'payment': payment,
        'amount': int(payment.amount)
    }
    return render(request, 'payment/payment.html', context)


@login_required
def payment_gateway(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
    except Payment.DoesNotExist:
        return redirect('shop:index')

    callback_url = request.build_absolute_uri(reverse('payment:payment_verify'))

    amount = int(payment.amount)
    if amount < 1000:
        amount = 1000

    # ===== ساختار جدید API v4 (حروف کوچک) =====
    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount * 10,  # v4 مبلغ رو به ریال میخواد، نه تومان (ضرب در ۱۰)
        "description": f"Order {payment.order.id}",
        "callback_url": callback_url,
    }

    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    print("=" * 50)
    print("DEBUG: Sending to Zarinpal v4:", data)

    try:
        response = requests.post(ZP_API_REQUEST, json=data, headers=headers, timeout=15)
        print("DEBUG: Status code:", response.status_code)
        print("DEBUG: Response text:", response.text[:500])

        result = response.json()
        print("DEBUG: Parsed result:", result)
        print("=" * 50)

        # در API v4 نتیجه داخل result['data'] هست
        result_data = result.get('data', {})

        if result_data.get('code') == 100:
            authority = result_data.get('authority')
            payment.authority = authority
            payment.save()
            return redirect(f"{ZP_API_STARTPAY}{authority}")
        else:
            errors = result.get('errors', {})
            error_message = f"خطای زرین‌پال: {errors}"
            print("DEBUG ERROR:", error_message)
            return render(request, 'payment/payment-failed.html', {
                'message': error_message
            })
    except requests.exceptions.RequestException as e:
        print("DEBUG EXCEPTION:", str(e))
        return render(request, 'payment/payment-failed.html', {
            'message': f'خطا در برقراری ارتباط: {str(e)}'
        })
    except Exception as e:
        print("DEBUG GENERAL EXCEPTION:", str(e))
        return render(request, 'payment/payment-failed.html', {
            'message': f'خطای نامشخص: {str(e)}'
        })


@login_required
def payment_verify(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')

    try:
        payment = Payment.objects.get(authority=authority)
    except Payment.DoesNotExist:
        return render(request, 'payment/payment-failed.html', {
            'message': 'پرداخت یافت نشد'
        })

    if status != 'OK':
        payment.status = 'cancelled'
        payment.save()
        return render(request, 'payment/payment-failed.html', {
            'message': 'پرداخت توسط شما لغو شد.',
            'payment': payment
        })

    data = {
        "merchant_id": MERCHANT_ID,
        "amount": int(payment.amount) * 10,
        "authority": authority,
    }
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    try:
        response = requests.post(ZP_API_VERIFY, json=data, headers=headers, timeout=15)
        result = response.json()
        result_data = result.get('data', {})

        if result_data.get('code') in (100, 101):
            payment.status = 'completed'
            payment.transaction_id = result_data.get('ref_id')
            payment.save()

            payment.order.status = 'paid'
            payment.order.save()

            return render(request, 'payment/payment-success.html', {
                'order': payment.order,
                'payment': payment
            })
        else:
            payment.status = 'failed'
            payment.save()
            return render(request, 'payment/payment-failed.html', {
                'message': 'پرداخت ناموفق بود. لطفاً دوباره تلاش کنید.',
                'payment': payment
            })
    except requests.exceptions.RequestException:
        return render(request, 'payment/payment-failed.html', {
            'message': 'خطا در تایید تراکنش. با پشتیبانی تماس بگیرید.',
            'payment': payment
        })