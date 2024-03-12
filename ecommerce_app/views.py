from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import UserForm, ProductForm
from .models import User, Cart, Product, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import jsons
import base64
import requests
import shortuuid
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from datetime import datetime
from django.views.decorators.cache import cache_control
from django.db.models import Count

# Create your views here.


########### Home, UserRegistration and Login ################
def home(request):
    products = Product.objects.all()
    # cart = Cart.objects.all()
    cart_product_id = []
    top_two = []
    quantity = 0
    if request.user.is_authenticated:
        user_id = request.user.id
        quantity = Cart.objects.filter(user_id=user_id).count()

        cart_filter = Cart.objects.filter(user_id=user_id)
        for id in cart_filter:
            cart_product_id.append(id.product_id)

    product_counts = Order.objects.values('product').annotate(product_count=Count('product')).order_by('-product_count')[:2]
    for i in product_counts:
        product = Product.objects.get(pk=i['product'])
        top_two.append(product)


    # print(cart_id)
    context = {
        'products': products,
        'quantity': quantity,
        'cart_product_id': cart_product_id,
        'top_two' : top_two
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
    cart = Cart.objects.filter(user_id=user_id)

    quantity = Cart.objects.filter(user_id=user_id).count()
    
    total_price = 0
    for item in cart:
        total_price += item.total_price
    
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
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(id=request.user.id)
            user_id = user.id
            username = request.POST['username']
            user.username = username
            user.save()
            return redirect('ecommerce:profile_page', profile_id=user_id)
    return render(request, 'update_username.html')

@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user_id = user.id

        if request.FILES:
            existing_pro_pic = user.profile_picture
            existing_pro_pic.delete(save=True)
            profile_picture = request.FILES['profile_picture']
            user.profile_picture = profile_picture
            user.save()
            return redirect('ecommerce:profile_page', profile_id=user_id)
        else:
            return HttpResponse('Please select a file')
        
    return render(request, 'update_profile_pic.html')
@login_required
def change_password(request):
    pass

@login_required
def password_change_done(request):
    return redirect('ecommerce:home')

@login_required
def proceed_to_checkout(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    total_price = 0
    for item in cart:
        total_price += item.total_price
    context = {
        'cart_items': cart,
        'total_price': total_price
    }
    return render(request, 'payment.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    response = redirect('ecommerce:home')
    response.delete_cookie('csrftoken')
    return response

################################## Phone Pay integration ########################################

############### Helper Function ################
def calculate_sha256_string(input_string):
    # Create a hash object using the SHA-256 algorithm
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Update hash with the encoded string
    sha256.update(input_string.encode('utf-8'))
    # Return the hexadecimal representation of the hash
    return sha256.finalize().hex()
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def base64_encode(input_dict):
    # Convert the dictionary to a JSON string
    json_data = jsons.dumps(input_dict)
    # Encode the JSON string to bytes
    data_bytes = json_data.encode('utf-8')
    # Perform Base64 encoding and return the result as a string
    return base64.b64encode(data_bytes).decode('utf-8')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
########################## Create your views here. ########################
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# def index(request):
#     return render(request, "index.html", { 'output': "Please Pay & Repond From The Payment Gateway Will Come In This Section", 'main_request': "" })

@login_required
def pay(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    total_price = 0
    for item in cart:
        total_price += int(item.total_price)
    MAINPAYLOAD = {
        "merchantId": "PGTESTPAYUAT",
        "merchantTransactionId": shortuuid.uuid(),
        "merchantUserId": "MUID123",
        "amount": total_price*100,
        "redirectUrl": "http://127.0.0.1:8000/return-to-me/",
        "redirectMode": "POST",
        "callbackUrl": "http://127.0.0.1:8000/return-to-me/",
        "mobileNumber": "9999999999",
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SETTING
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    INDEX = "1"
    ENDPOINT = "/pg/v1/pay"
    SALTKEY = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    base64String = base64_encode(MAINPAYLOAD)
    mainString = base64String + ENDPOINT + SALTKEY
    sha256Val = calculate_sha256_string(mainString)
    checkSum = sha256Val + '###' + INDEX
    # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # # Payload Send
    # # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    headers = {
        'Content-Type': 'application/json',
        'X-VERIFY': checkSum,
        'accept': 'application/json',
    }
    json_data = {
        'request': base64String,
    }
    response = requests.post('https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay', headers=headers, json=json_data)
    responseData = response.json()
    cart = Cart.objects.filter(user_id=request.user.id)
    for item in cart:
        Order.objects.create(
                user_id=request.user.id,
                product_id=item.product_id,
                quantity=item.quantity,
                total_price=item.total_price,
                order_date=datetime.today().strftime('%Y-%m-%d')
            )

        item.delete()
    return redirect(responseData['data']['instrumentResponse']['redirectInfo']['url'])



# def success(request,response_dict):
#         transact_id = response_dict['data']['transactionId']
#         amount = response_dict['data']['amount']
        
#         # Get the user ID
#         user_id = request.user.id
#         print("Successs:",user_id)

#         # Get cart items for the user
#         cart_items = Cart.objects.filter(user_id=user_id)

#         # Create orders and prepare a list of items to delete
#         items_to_delete = []
#         for item in cart_items:
#             Order.objects.create(
#                 user_id=user_id,
#                 product_id=item.product_id,
#                 quantity=item.quantity,
#                 total_price=item.total_price,
#                 order_date=datetime.today().strftime('%Y-%m-%d')
#             )
#             items_to_delete.append(item)

#         # Delete the items from the cart
#         for item in items_to_delete:
#             item.delete()

    # else:
    #     # Handle the case when the payment is not successful
    #     # You may want to log or handle this accordingly
    #     pass



@csrf_exempt
def payment_return(request):

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # SETTING
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    INDEX = "1"
    SALTKEY = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Access form data in a POST request
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_data = request.POST
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Convert form data to a dictionary
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_data_dict = dict(form_data)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    transaction_id = form_data.get('transactionId', None)
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 1.In the live please match the amount you get byamount you send also so that hacker can't pass static value.
    # 2.Don't take Marchent ID directly validate it with yoir Marchent ID
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if transaction_id:
        request_url = 'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT/' + transaction_id;
        sha256_Pay_load_String = '/pg/v1/status/PGTESTPAYUAT/' + transaction_id + SALTKEY;
        sha256_val = calculate_sha256_string(sha256_Pay_load_String)
        checksum = sha256_val + '###' + INDEX
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Payload Send
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
            'X-MERCHANT-ID': transaction_id,
            'accept': 'application/json',
        }
        response = requests.get(request_url, headers=headers)
        response_dict = jsons.loads(response.text)
        # success(request,response_dict)

        if response_dict['code'] == 'PAYMENT_SUCCESS':
            transact_id = response_dict['data']['transactionId']
            amount = response_dict['data']['amount']
            return render(request, 'payment_success.html', { 'transact_id': transact_id, 'amount': amount})
        
        else:
            return render(request, 'payment_failed.html')
        
            # transact_id = response.text['transactionId']
            # return render(request, 'payment_success.html', { 'output': response.text, 'main_request': form_data_dict  })
    # return render(request, 'payment_success.html', { 'output': response.text, 'main_request': form_data_dict  })

            # Order.objects.create(user_id=request.user.id, product_id=item.product_id, quantity=item.quantity, total_price=item.total_price, order_date = datetime.today().strftime('%Y-%m-%d'))
            # item.delete()
