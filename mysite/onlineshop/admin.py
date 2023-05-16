from django.contrib import admin
from .models import Status, Customer, Product, Order, OrderItem, ShippingAddress

class OrderItemInItem(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_ordered', 'status']
    inlines = [OrderItemInItem]
    list_filter = ['status']

# Register your models here.
admin.site.register(Status)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
