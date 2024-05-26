from django.urls import path
from . import views



urlpatterns= [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_details, name='vendor_details'),

    #add to cart
    path('add-to-cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
]