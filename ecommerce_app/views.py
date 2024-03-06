from django.shortcuts import render, redirect, reverse
from .forms import UserForm, ProductForm
from .models import User, Cart, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


# HOME, UserRegistration and Login
def home(request):
    products = Product.objects.all()
    cart = Cart.objects.all()
    cart_none = Cart.objects.none()
    c_cart = list(cart.union(cart_none))
    print(c_cart)

    print(c_cart)
    quantity = 0
    if request.user.is_authenticated:
        user_id = request.user.id
        quantity = Cart.objects.filter(user_id=user_id).count()
    
    context = {
        'products': products,
        'quantity': quantity,
        'cart': cart
    }
    return render(request, 'home.html', context)


def register_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

        form = UserForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        products = Product.objects.all()
        context = {
            'products': products
        }
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html', context)
        else:
            return messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')



def product_register(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print("hiii")
            form.save()
        form = ProductForm()
        return render(request, 'product_register.html', {'form':form})
    return render(request, 'product_register.html', {'form': form})


##### cart #####
@login_required
def add_to_cart(request,product_pk):
    if request.user.is_authenticated:
        price = Product.objects.get(pk=product_pk).product_price
        user_id = request.user.id
        product_id = product_pk
        Cart.objects.create(user_id=user_id, product_id=product_id, price=price, total_price=1*price)

        quantity = Cart.objects.filter(user_id=user_id).count()
        context = {
            'quantity': quantity
        }
        return redirect(reverse('ecommerce:home') + f'?quantity={quantity}')
    return render(request, 'home.html')

@login_required
def go_to_cart(request):
    user_id = request.user.id
    print(user_id)
    cart = Cart.objects.filter(user_id=user_id)

    quantity = Cart.objects.filter(user_id=user_id).count()

    for i in cart:
        print(i.id)
    print(cart)
    
    total_price = 0
    for item in cart:
        total_price += item.total_price
        print(total_price)
    
    context = {
        'cart_items': cart,
        'total_price': total_price,
        'quantity': quantity
    }
    return render(request, 'cart.html', context)

@login_required
def increase_cart_items(request, cart_pk):
    cart = Cart.objects.get(pk=cart_pk)
    cart.quantity += 1
    cart.total_price = cart.price * cart.quantity
    cart.save()
    return redirect('ecommerce:go_to_cart')

@login_required
def decrease_cart_items(request, cart_pk):
    cart = Cart.objects.get(pk=cart_pk)
    cart.quantity -= 1
    cart.total_price -= cart.price
    cart.save()
    return redirect('ecommerce:go_to_cart')


@login_required
def remove_from_cart(request, cart_pk):
    cart = Cart.objects.get(pk=cart_pk)
    cart.delete()
    return redirect('ecommerce:go_to_cart')



