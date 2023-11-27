import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, send_mail
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, FormView, DetailView

from store_kashpo.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL
from . import utils
from .forms import ContactForm, RegisterForm
from .models import Product, Order, OrderItem, ShippingAddress, Customer, Galary, Color
from .utils import guestOrder, get_order_info


def store(request):

    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']

    csrf_token = get_token(request)
    products_kashpo = Product.objects.all().filter(is_active=True, category=1)[:4].select_related('category')
    products_rack = Product.objects.all().filter(is_active=True, category=3)[:4].select_related('category')
    products_metal_furniture = Product.objects.all().filter(is_active=True, category=2)[:4].select_related('category')
    products_interior = Product.objects.all().filter(is_active=True, category=4)[:4].select_related('category')
    products_rotang_furniture = Product.objects.all().filter(is_active=True, category=5)[:4].select_related('category')
    context = {
        "products_kashpo": products_kashpo,
        "products_rack":products_rack,
        "products_metal_furniture":products_metal_furniture,
        "products_interior":products_interior,
        "products_rotang_furniture": products_rotang_furniture,
        'title' : 'Главная',
        "cartItems":cartItems,

    }

    return render(request, 'store/store.html',context = context )


def cart(request):
    if request.user.is_authenticated:
        data = utils.cartData(request)
        order = data['order']
        items = data['items']
        cartItems = data['cartItems']
        shipping = data['shipping']
    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']
        order = cookiesCart['order']
        items = cookiesCart['items']
        shipping = cookiesCart['shipping']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'shipping': shipping,
        'title':'Корзина'}
    return render(request,'store/cart.html',context)

def checkout(request):


    if request.user.is_authenticated:
        data = utils.cartData(request)
        order = data['order']
        items = data['items']
        cartItems = data['cartItems']
        shipping = data['shipping']
    else:
        cookiesCart = utils.cookiesCart(request)


        print(['items'])
        cartItems = cookiesCart['cartItems']
        order = cookiesCart['order']
        items = cookiesCart['items']
        shipping = cookiesCart['shipping']

    context = {'items': items,
               'order': order,
               'cartItems': cartItems,
               'shipping': shipping,
               'title':'Оформление'}
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

    if orderItem.quantity <= 0 or action == 'del':
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

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
                phone=data['shipping']['phone'],
            )

    else:
        print('User is not logged in...')
        print('COOKIES: ', request.COOKIES)

        customer, order = guestOrder(request, data)

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                country=data['shipping']['country'],
                zipcode=data['shipping']['zipcode'],
                phone=data['shipping']['phone'],
            )

    head, sep, tail = data['form']['total'].partition(',')
    total = float(head)
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    return JsonResponse('Payment submitted..', safe=False)


class CategoryView(ListView):
    model = Product
    template_name = 'store/category.html'
    context_object_name = 'products_by_category'

    def get_queryset(self):

        return Product.objects.filter(category_id=self.kwargs['pk'], is_active=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data = utils.cartData(self.request)
            context['cartItems'] = data['cartItems']
        else:
            cookiesCart = utils.cookiesCart(self.request)
            context['cartItems'] = cookiesCart['cartItems']
        return context

def  contact(request):
    print(request.META.get('PATH_INFO', None))
    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']

    if request.method == 'GET':
        form = ContactForm()

    elif request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(f'{subject} от {from_email}', message)
                # send_mail(f'{subject} от {from_email}', message,
                #        DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)

            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return redirect('/success')
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "store/contact.html", {'form': form, 'cartItems': cartItems, 'title':'Контакты'})

def success_email(request):
    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']
    return render(request,'store/success-email.html',{'cartItems': cartItems, 'title':'Спасибо'})

@login_required
def profile_view(request):
    title='Профиль'
    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']

    list_orders = Order.objects.filter(customer=request.user.customer,complete=True)
    order_info = get_order_info(list_orders)
    order_info = {'order_info':order_info,'cartItems': cartItems,'title':title}
    return render(request, 'registration/profile.html',context=order_info)

def login(request):
    return render(request, 'registration/login.html')

def color(request):
    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']

    colors = Color.objects.all()
    return render(request, 'store/color.html',{'title':'Цвета ротанга','cartItems':cartItems, "colors": colors})



class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile_view')
    extra_context = {"title":'Регистрация'}

    def form_valid(self, form):
        form.save()
        new_user = User.objects.get(username=form.cleaned_data['username'])
        new_customer = Customer(name=form.cleaned_data['first_name'],email=form.cleaned_data['email'],last_name=form.cleaned_data['last_name'])
        new_user.customer = new_customer
        new_user.customer.save()

        return super().form_valid(form)

@cache_page(60 * 15)
def galary(request):
    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']

    arr = Galary.objects.all()
    return render(request, 'store/galary.html', {'title': 'Гaлерея', 'cartItems': cartItems, 'arr': arr})

def about(request):
    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']

    return render(request, 'store/about.html', {'title': 'О нас', 'cartItems': cartItems})

def conditions(request):
    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']

    return render(request, 'store/conditions.html', {'title': 'Условия', 'cartItems': cartItems})

def agreement(request):
    if request.user.is_authenticated:
        data = utils.cartData(request)
        cartItems = data['cartItems']

    else:
        cookiesCart = utils.cookiesCart(request)
        cartItems = cookiesCart['cartItems']

    return render(request, 'store/agreement.html', {'title': 'Соглашение', 'cartItems': cartItems})

class ProductDetail(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data = utils.cartData(self.request)
            context['cartItems'] = data['cartItems']
        else:
            cookiesCart = utils.cookiesCart(self.request)
            context['cartItems'] = cookiesCart['cartItems']
        return context

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h2>Страница не найдена</h2')