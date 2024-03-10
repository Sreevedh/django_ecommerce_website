from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import UserForm, ProductForm
from .models import User, Cart, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.


########### Home, UserRegistration and Login ################
def home(request):
    products = Product.objects.all()
    cart = Cart.objects.all()
    cart_product_id = []
    quantity = 0
    if request.user.is_authenticated:
        user_id = request.user.id
        quantity = Cart.objects.filter(user_id=user_id).count()

        cart_filter = Cart.objects.filter(user_id=user_id)
        for id in cart_filter:
            cart_product_id.append(id.product_id)

    # print(cart_id)
    context = {
        'products': products,
        'quantity': quantity,
        'cart_product_id': cart_product_id
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


################### Cart ################
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
    if cart.quantity == 0:
        cart = Cart.objects.get(pk=cart_pk)
        cart.delete()
        return redirect('ecommerce:go_to_cart')
    
    cart.total_price -= cart.price
    cart.save()
    return redirect('ecommerce:go_to_cart')


@login_required
def remove_from_cart(request, cart_pk):
    cart = Cart.objects.get(pk=cart_pk)
    cart.delete()
    return redirect('ecommerce:go_to_cart')

##################### Product Details Page ##################

def product_detail_tab(request, product_id):
    # product = get_object_or_404(Product, id=product_id)
    product = Product.objects.get(id = product_id)
    cart_list = []
    user_id = request.user.id
    quantity = Cart.objects.filter(user_id=user_id).count()
    if request.user.is_authenticated:
        user_id = request.user.id
        cart_product_id = Cart.objects.filter(user_id = user_id)
        for i in cart_product_id:
            cart_list.append(i.product_id)
    
    context = {
        'product': product,
        'cart':cart_list,
        'quantity':quantity
     }
    return render(request, 'product_details.html', context)



############################## Profile Page ######################################
@login_required
def profile_page(request, profile_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk = profile_id)
        quantity = Cart.objects.filter(user_id = profile_id).count()
        context ={
            'user':user,
            'quantity':quantity
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('ecommerce:home')

@login_required  
def update_username(request):
    pass

@login_required
def change_profile_picture(request):
    pass

@login_required
def change_password(request):
    pass

@login_required
def password_change_done(request):
    return HttpResponse('Success')


