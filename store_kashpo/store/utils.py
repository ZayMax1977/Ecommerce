import json
from .models import Product, Order, Customer, OrderItem


def cookiesCart(request,shipping=False):
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

    return {'items': items, 'order': order, 'cartItems': cartItems, 'shipping': shipping}

def cartData(request,shipping=False):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items
    return{'items': items, 'order': order, 'cartItems': cartItems, 'shipping': shipping}

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
