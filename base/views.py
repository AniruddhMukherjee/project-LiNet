from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import ProductForm


# Create your views here.

# products = [
#    {'id': 1, 'name': 'PRODUCT 1'},
#    {'id': 2, 'name': 'PRODUCT 2'},
#    {'id': 3, 'name': 'PRODUCT 3'},
# ]

# ------------------------------------------------------------------------- Login Page
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username/password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


# ------------------------------------------------------------------------- Logout user
def logoutUser(request):
    logout(request)
    return redirect('home')


# ------------------------------------------------------------------------- register user
def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})


# ------------------------------------------------------------------------- home page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    products = Sell.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        # Q(user__icontains=q)
    )


    topics = Topic.objects.all()
    announcements = Announcement.objects.all()
    product_count = products.count()
    context = {'products': products, 'topics': topics,
               'product_count': product_count,
               'announcements': announcements}
    return render(request, 'base/home.html', context)


# ------------------------------------------------------------------------- product info
def product(request, pk):
    product = Sell.objects.get(id=pk)
    Productmessages = product.messages_set.all().order_by('-created')

    if request.method == 'POST':
        message = Messages.objects.create(
            user=request.user,
            product=product,
            body=request.POST.get('body')
        )
        return redirect('product', pk=product.id)



    context = {'product': product, 'messages': Productmessages}
    return render(request, 'base/product.html', context)

# -------------------------------------------------------------------------user profile
def userProfile(request,pk):
    users = User.objects.get(id=pk)
    context = {'users': users}
    return render(request, 'base/profile.html', context)

# ------------------------------------------------------------------------- new product
@login_required(login_url='/login')
def NewProduct(request):  # to create
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/product_form.html', context)


# ------------------------------------------------------------------------- user profile
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'base/profile.html', context)


# ------------------------------------------------------------------------- update product
@login_required(login_url='/login')
def UpdateProduct(request, pk):  # update the product
    product = Sell.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.user != product.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/product_form.html', context)


# ------------------------------------------------------------------------- delete product
@login_required(login_url='/login')
def DeleteProduct(request, pk):
    product = Sell.objects.get(id=pk)

    if request.user != product.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': product})
