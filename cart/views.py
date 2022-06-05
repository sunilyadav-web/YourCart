import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse

def store(request):
    if request.user.is_authenticated:
        customer=request.user
        cart,created=Cart.objects.get_or_create(owner=customer,completed=False)
        cartitems=cart.cartitems_set.all()
    else:
        cart=[]
        cartitems=[]
        cart={'cartquantity':0}

    products=Prodcut.objects.all()
    context={'products':products,'cart':cart,'cartitems':cartitems}

    return render(request,'cart/home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user
        cart,created=Cart.objects.get_or_create(owner=customer,completed=False)
        cartitems=cart.cartitems_set.all()
    else:
        cart=[]
        cartitems=[]
        cart={'cartquantity':0}
    context={'cartitems':cartitems,'cart':cart}
    return render(request,'cart/cart.html',context)

def checkOut(request):
    return render(request,'cart/checkout.html')

def addToCart(request):
    data=json.loads(request.body)
    product_id=data['product_id']
    action=data['action']
    if request.user.is_authenticated:
        customer=request.user
        product=Prodcut.objects.get(product_id=product_id)
        cart, created=Cart.objects.get_or_create(owner=customer,completed=False)
        cartitems, created=Cartitems.objects.get_or_create(product=product,cart=cart)

        if action=="add":
            cartitems.quantity += 1
        cartitems.save()
        msg={
            'quantity':cart.cartquantity
        }

    return JsonResponse(msg,safe=False)

def signin(request):
    if request.user.is_authenticated:
        messages.error(request,'You already logged in.')
        return redirect(store)

    if request.method == "POST":
        username=request.POST['username']
        pass1=request.POST['pass1']

        if username == '':
            messages.error(request,"Please Enter a Username")
            return redirect(store)

        if pass1 == '':
            messages.error(request,"Please Enter a Password")
            return redirect(store)

        check_user=User.objects.filter(username=username).first()
        if check_user is None:
            messages.error(request,'Invalid username not found. Please enter a valid username.')
            return redirect(store)

        user=authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            messages.success(request,'You are logged in successfully !')
            return redirect('store')
        else:
            messages.error(request,'Invalid password. Please enter a valid password!')
            return redirect('store')
    else:
        messages.error(request,'Somthing went wrong.')
        return redirect(store) 


def register(request):
    try:
        if request.method == 'POST':
            username=request.POST['username']
            fname=request.POST['fname']
            lname=request.POST['lname']
            email=request.POST['email']
            pass1=request.POST['pass1']
            pass2=request.POST['pass2']

            if username == '':
                messages.error(request,'Username is must.')
                return redirect(store)

            if fname == '':
                messages.error(request,'First Name is Mandatory')
                return redirect(store)

            if lname == '':
                messages.error(request,'Last Name is Mandatory')
                return redirect(store)

            if email == '':
                messages.error(request,'Email is compalsary.')
                return redirect(store)

            if pass1 != pass2:
                messages.error(request,'Both password should be match')
                return redirect(store)
                
            user_obj=User.objects.filter(username=username)
            if user_obj:
                messages.error(request,'Username is already Exit!')
                return redirect(store)
                
            myuser=User.objects.create_user(username,email,pass1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()

            messages.success(request,"Your Account has been created successfully!")

            return redirect('store')
    except Exception as e:
        print(e)
    return HttpResponse(' 404 Page not found ')

def signout(request):
    logout(request)
    messages.success(request,'You are logged out successfully!')
    return redirect('store')

