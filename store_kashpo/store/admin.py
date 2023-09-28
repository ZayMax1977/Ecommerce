from django.contrib import admin

from store.models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

    class Meta:
        model = Category

admin.site.register(Category,CategoryAdmin)

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
# admin.site.register(Category)