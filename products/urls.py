from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.search_products, name='search'),
    path('category/<str:slug>/', views.category_products, name='category'),
    path('product/<str:slug>/', views.product_detail, name='product_detail'),
    path('live-search/', views.live_search, name='live_search'),
]