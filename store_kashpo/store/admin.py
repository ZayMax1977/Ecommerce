from django.contrib import admin
from .models import *

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]
    inlines = [OrderItemInline]
    class Meta:
        model = Order
admin.site.register(Order,OrderAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields]
    inlines = [OrderInline]
    class Meta:
        model = Customer
admin.site.register(Customer,CustomerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    class Meta:
        model = Category
admin.site.register(Category,CategoryAdmin)

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ShippingAddress._meta.fields if field.name != "id"]
    class Meta:
        model = ShippingAddress
admin.site.register(ShippingAddress,ShippingAddressAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    class Meta:
        model = Product
admin.site.register(Product,ProductAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','product','color','order','quantity']
    class Meta:
        model = OrderItem
admin.site.register(OrderItem,OrderItemAdmin)

class GalaryAdmin(admin.ModelAdmin):
    list_display = ['title']
    class Meta:
        model = Galary
admin.site.register(Galary,GalaryAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display = ['title']
    class Meta:
        model = Color
admin.site.register(Color,ColorAdmin)