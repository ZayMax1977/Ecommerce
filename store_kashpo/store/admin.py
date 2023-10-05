from django.contrib import admin
from store.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

    class Meta:
        model = Category

admin.site.register(Category,CategoryAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','product','color','order','quantity']

    class Meta:
        model = OrderItem

admin.site.register(OrderItem,OrderItemAdmin)


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ShippingAddress)
