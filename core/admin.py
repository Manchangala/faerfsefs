from django.contrib import admin
from .models import Category, Product, Customer, DeliveryPerson, Order, OrderItem, Delivery

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(DeliveryPerson)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Delivery)
