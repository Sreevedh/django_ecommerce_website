from django.contrib import admin
from django.urls import path
from .views import home, register_user, login_user, product_register, add_to_cart, go_to_cart, increase_cart_items, decrease_cart_items, remove_from_cart, product_detail_tab, profile_page, password_change_done, update_profile_pic, update_username, pay, payment_return, proceed_to_checkout, logout_view

from django.contrib.auth import views as auth_views
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
    path('product_detail/<int:product_id>/',product_detail_tab,name='product_detail_tab'),
    path('profile_page/<int:profile_id>',profile_page, name='profile_page'),
    path('update_profile_pic/',update_profile_pic, name='update_profile_pic'),
    path('update_username/',update_username, name='update_username'),

    # path('change_password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'))
      path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='/change-password/done/'
    ), name='password_change'),

     path('change-password/done/', password_change_done, name='password_change_done'),

     path('proceed-to-checkout/', proceed_to_checkout, name='proceed_to_checkout'),
     path('return-to-me/', payment_return, name='payment_return'),
     path('pay/', pay, name='pay'),
     path('logoutpage/', logout_view, name='logout')
    #  path('add_to_cart_in')

]