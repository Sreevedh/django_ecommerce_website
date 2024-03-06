from django.contrib import admin
from django.urls import path
from .views import home, register_user, login_user, product_register, add_to_cart, go_to_cart, increase_cart_items, decrease_cart_items, remove_from_cart


app_name = 'ecommerce_app'
urlpatterns = [
    path('', home, name='home'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('product_register/', product_register, name='product_register'),
    path('add_to_cart/<int:product_pk>/', add_to_cart, name='add_to_cart'),
    path('go_to_cart/', go_to_cart, name='go_to_cart'),
    path('increase_cart_items/<int:cart_pk>/', increase_cart_items, name='increase_cart_items'),
    path('decrease_cart_items/<int:cart_pk>/', decrease_cart_items, name='decrease_cart_items'),
    path('remove_from_cart/<int:cart_pk>/', remove_from_cart, name='remove_from_cart'),

]