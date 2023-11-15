import json
from .models import Product, Order, Customer, OrderItem, ShippingAddress


def cookiesCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    # get_cart_items - общее кол.единиц товара
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']


    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            # получаем id товара из ключа откидывая все кроме числа
            id = int(i.replace(i[i.find("_"):], ''))
            product = Product.objects.get(id=id)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,

                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
                'color': cart[i]['color'],
            }
            items.append(item)
            if product.digital == False:
                shipping = True
        except:
            pass

    return {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': True}

def cartData(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    return{'items': items, 'order': order, 'cartItems': cartItems, 'shipping': False}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookiesCart(request)
    items = cookieData['items']


    customer, created = Customer.objects.get_or_create(
            email=email,
            )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
        )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
            color=item['color'],
        )
    return customer, order

def get_order_info(list_orders):
    order_info = {}
    num = 0
    for i in list_orders:
        order_info['order_' + str(i.id)] = {}
        order_info['order_' + str(i.id)]['date_ordered'] = i.date_ordered
        order_info['order_' + str(i.id)]['complete'] = i.complete
        order_info['order_' + str(i.id)]['sent'] = i.sent
        shipping_info = ShippingAddress.objects.filter(order=list_orders[num].id)
        for j in shipping_info:
            order_info['order_' + str(i.id)]['id'] = list_orders[num].id
            order_info['order_' + str(i.id)]['address'] = j.address
            order_info['order_' + str(i.id)]['city'] = j.city
            order_info['order_' + str(i.id)]['state'] = j.state
            order_info['order_' + str(i.id)]['country'] = j.country
            order_info['order_' + str(i.id)]['zipcode'] = j.zipcode
        num += 1

    for i in order_info:
        order_info[i]['products'] = {}
        num = 1
        for j in OrderItem.objects.filter(order=i[6:]):
            order_info[i]['products']['product' + str(num)] = j.product.name+', '+str(j.quantity)+'шт. '+'Цвет: '+j.color
            num += 1

    return order_info