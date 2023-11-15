from django.urls import path
from .views import *

urlpatterns = [
    path('',store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', updateItem, name="update_item"),
    path('process_order/', processOrder, name="process_order"),
    path('category/<int:pk>/', CategoryView.as_view(), name="category"),
    path('contact/', contact, name="contact"),
    path('success/', success_email, name="success_email"),
    path('profile/', profile_view, name="profile_view"),
    path('login/', login, name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('color/', color, name='color'),
    path('galary/', galary, name='galary'),
    path('about/', about, name='about'),

]