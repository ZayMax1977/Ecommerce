import json

from django.http import JsonResponse
from django.shortcuts import render

from store.models import Product, Order, OrderItem


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all().filter(is_active=True)
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0} # Это для вывода в шаблон для
        # неавторизованного пользователя, иначе выйдет ошибка. Пока так
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}  # Это для вывода в шаблон для
        # неавторизованного пользователя, иначе выйдет ошибка. Пока так
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order,'cartItems': cartItems, 'shipping': False}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    print(order)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    print(orderItem)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)