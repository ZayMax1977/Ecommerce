import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.middleware.csrf import get_token
from . import utils
from .models import Product, Order, OrderItem, ShippingAddress, Customer
from .utils import guestOrder


def store(request):
    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']

    csrf_token = get_token(request)
    products = Product.objects.all().filter(is_active=True)
    context = {'products': products, 'cartItems': cartItems, 'csrf_token': csrf_token}
    return render(request, 'store/store.html', context)


def cart(request):
    shipping = False
    if request.user.is_authenticated:
        data = utils.cartData(request,shipping)
        order = data['order']
        items = data['items']
        cartItems = data['cartItems']
        shipping = data['shipping']
    else:
        cookiesCart = utils.cookiesCart(request,shipping)
        cartItems = cookiesCart['cartItems']
        order = cookiesCart['order']
        items = cookiesCart['items']
        shipping = cookiesCart['shipping']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': shipping}
    return render(request,'store/cart.html',context)

def checkout(request):
    shipping = False
    if request.user.is_authenticated:
        data = utils.cartData(request,shipping)
        order = data['order']
        items = data['items']
        cartItems = data['cartItems']
        shipping = data['shipping']
    else:
        cookiesCart = utils.cookiesCart(request, shipping=False)


        print(['items'])
        cartItems = cookiesCart['cartItems']
        order = cookiesCart['order']
        items = cookiesCart['items']
        shipping = cookiesCart['shipping']

    context = {'items': items, 'order': order,'cartItems': cartItems, 'shipping': shipping}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    color = data['color']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, color=color)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('Transaction_id: ',transaction_id)
    print('Data:', data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)


        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                country=data['shipping']['country'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in...')
        print('COOKIES: ', request.COOKIES)

        customer, order = guestOrder(request, data)

        print()

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            country=data['shipping']['country'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)