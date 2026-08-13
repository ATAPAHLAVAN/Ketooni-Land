from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('order/<int:order_id>/', views.payment_page, name='payment_page'),
    path('verify/', views.payment_verify, name='payment_verify'),
    path('gateway/<int:payment_id>/', views.payment_gateway, name='gateway'),
]