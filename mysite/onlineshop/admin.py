from django.contrib import admin
from .models import Status, Customer, Product, Order, OrderItem, ShippingAddress

# Register your models here.
admin.site.register(Status)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
