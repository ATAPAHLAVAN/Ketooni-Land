from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('addresses/', views.addresses_view, name='addresses'),
    path('address/add/', views.add_address, name='add_address'),
    path('logout/', views.logout_view, name='logout'),
]