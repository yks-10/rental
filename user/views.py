from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import UserForm, ProductForm, OrderForm
from .models import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    return render(request, 'user/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'user/signupuser.html', {'form': UserForm()})
    else:
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password'],
                    name=request.POST['username'],
                    phone_number=request.POST['phone_number'],  # Corrected field name
                    email=request.POST['email']
                )
                user.save()
                login(request, user)
                return redirect('user:productlist')
            except IntegrityError:
                return render(request, 'user/signupuser.html', {'form': UserForm(), 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'user/signupuser.html', {'form': UserForm(), 'error': 'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'user/loginuser.html', {'form': AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print("Authenticated User:", user)
        if user is None:
            return render(request, 'user/loginuser.html', {'form': AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('user:productlist')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'user/home.html')

def productlist(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'user/products.html', {'products': products})

def productdetails(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == 'GET':
        form = ProductForm(instance=product)
        return render(request, 'user/productdetails.html', {'product': product, 'form': form})

    elif request.method == 'POST':
        try:
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('user:productlist')
            else:
                return render(request, 'user/productdetails.html',
                              {'product': product, 'form': form, 'error': 'Invalid form data'})
        except ValueError:
            return render(request, 'user/productdetails.html',
                          {'product': product, 'form': form, 'error': 'Bad info'})


@login_required
def createproduct(request):
    if request.method == 'GET':
        return render(request, 'user/createproduct.html', {'form':ProductForm()})
    else:
        try:
            form = ProductForm(request.POST)
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('user:productlist')
        except ValueError:
            return render(request, 'user/createproduct.html', {'form':ProductForm(), 'error':'Bad data passed in. Try again.'})

@login_required
def deleteproduct(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if request.method == 'POST':
        product.delete()
        return redirect('user:productlist')


@login_required
def createorder(request):
    if request.method == 'POST':
        try:
            form = OrderForm(request.POST)
            if form.is_valid():
                selected_products = request.POST.getlist('selected_products')
                order = form.save(commit=False)
                order.user = request.user
                order.save()

                total_price = 0

                for product_id in selected_products:
                    product = get_object_or_404(Product, pk=product_id)
                    quantity = int(request.POST.get(f'quantity_{product_id}', 0))

                    OrderItem.objects.create(order=order, product=product, quantity=quantity)

                    # Calculate total price
                    total_price += float(product.price) * int(quantity)

                # Update the order's total price
                order.total_price = total_price
                order.save()

                messages.success(request, 'Your order has been placed successfully!')

                return redirect('user:productlist')
            else:
                return render(request, 'user/createorder.html', {'form': form, 'error': 'Invalid form data'})
        except ValueError:
            return render(request, 'user/createorder.html', {'form': OrderForm(), 'error': 'Bad data passed in. Try again.'})
    else:
        products = Product.objects.all()
        return render(request, 'user/createorder.html', {'products': products, 'form': OrderForm()})


@login_required
def orderlist(request):
    # Fetch all orders for the logged-in user and order them by creation date
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Pagination logic
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page = request.GET.get('page')
    try:
        orders_paginated = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        orders_paginated = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        orders_paginated = paginator.page(paginator.num_pages)

    return render(request, 'user/orderlist.html', {'orders': orders_paginated})

from django.shortcuts import render, get_object_or_404
from .models import Order
from django.contrib.auth.decorators import login_required

@login_required
def orderdetails(request, order_id):
    order = get_object_or_404(Order, unique_id=order_id, user=request.user)
    order_items = order.items.all()  # Fetch related OrderItems
    return render(request, 'user/orderdetails.html', {'order': order, 'order_items': order_items})
