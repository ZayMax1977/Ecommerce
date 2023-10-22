from django.urls import path

from . import views

from .views import CategoryView

urlpatterns = [
    path('',views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    # path('category/<int:pk>/', views.get_by_category, name="get_by_category")
    path('category/<int:pk>/', CategoryView.as_view(), name="category")

]