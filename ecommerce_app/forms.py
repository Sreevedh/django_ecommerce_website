from django import forms
from .models import User, Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField


class UserForm (UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2','profile_picture')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'product_details', 'product_price', 'product_image')
