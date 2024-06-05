from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Asegúrate de que haya un valor por defecto

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class DeliveryPerson(models.Model):
    name = models.CharField(max_length=200)
    vehicle_type = models.CharField(max_length=50)
    license_number = models.CharField(max_length=50, null=True, blank=True)  # Corrige aquí
    license_expiry = models.DateField(null=True, blank=True)
    availability_hours = models.JSONField()

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    address = models.TextField()
    delivery_person = models.ForeignKey(DeliveryPerson, null=True, blank=True, on_delete=models.SET_NULL)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.TextField()
    scheduled_time = models.DateTimeField()
    completed_time = models.DateTimeField(null=True, blank=True)


from django.utils import timezone
from .models import DeliveryPerson, Order

def assign_delivery_person(order):
    now = timezone.now()
    available_delivery_persons = DeliveryPerson.objects.filter(
        availability_hours__contains=[now.hour],
        license_expiry__gte=now
    ).order_by('id')

    if available_delivery_persons.exists():
        delivery_person = available_delivery_persons.first()
        order.delivery_person = delivery_person
        order.save()
        
        # Actualizar la cola (simplificado)
        delivery_persons_list = list(available_delivery_persons)
        delivery_persons_list.append(delivery_persons_list.pop(0))
        
        return delivery_person
    else:
        return None

