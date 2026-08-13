# File: reviews/views.py

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Review, ReviewVote


@login_required
@require_POST
def add_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    rating = request.POST.get('rating')
    comment = request.POST.get('comment')

    if not rating or not comment:
        messages.error(request, 'لطفا امتیاز و متن نظر را وارد کنید')
        return redirect('products:product_detail', slug=product_slug)

    review, created = Review.objects.update_or_create(
        product=product, user=request.user,
        defaults={'rating': int(rating), 'comment': comment}
    )

    if created:
        messages.success(request, 'نظر شما با موفقیت ثبت شد')
    else:
        messages.success(request, 'نظر شما بروزرسانی شد')

    return redirect('products:product_detail', slug=product_slug)


@login_required
@require_POST
def vote_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    is_like = request.POST.get('is_like') == 'true'

    vote, created = ReviewVote.objects.update_or_create(
        review=review, user=request.user,
        defaults={'is_like': is_like}
    )

    return JsonResponse({
        'success': True,
        'likes': review.like_count(),
        'dislikes': review.dislike_count(),
    })


@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, 'نظر شما حذف شد')
    return redirect('products:product_detail', slug=product_slug)