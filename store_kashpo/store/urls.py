from django.urls import path

from store import views
from store.views import store, cart, checkout

urlpatterns = [
    path('',store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
]