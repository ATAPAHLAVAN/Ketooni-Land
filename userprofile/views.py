from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from orders.models import Order
from .models import UserProfile, Address

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    addresses = Address.objects.filter(user=request.user)
    
    context = {
        'profile': profile,
        'orders': orders,
        'addresses': addresses,
        'total_orders': Order.objects.filter(user=request.user).count(),
    }
    
    return render(request, 'userprofile/profile.html', context)

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        profile.bio = request.POST.get('bio', '')
        profile.phone = request.POST.get('phone', '')
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        
        return redirect('userprofile:profile')
    
    context = {'profile': profile}
    return render(request, 'userprofile/edit_profile.html', context)

@login_required
def addresses_view(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'userprofile/addresses.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            is_default=request.POST.get('is_default') == 'on'
        )
        return redirect('userprofile:addresses')
    
    return render(request, 'userprofile/add_address.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('shop:index')