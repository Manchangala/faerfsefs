from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Cart, CartItem, Order, OrderItem, Customer
from .forms import CartItemForm, OrderForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil de cliente
            Customer.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('menu')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out')
    return redirect('home')

def menu(request):
    if not request.user.is_authenticated:
        return redirect('login')
    products = Product.objects.all()
    return render(request, 'core/menu.html', {'products': products})

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        # Asegurarse de que quantity tenga un valor por defecto de 1 si está vacío
        if not quantity:
            quantity = 1

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        
        # Obtener o crear un CartItem con un valor por defecto de 0 para quantity
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
        
        # Actualizar la cantidad del CartItem
        cart_item.quantity += int(quantity)
        cart_item.save()

        messages.success(request, f'Added {quantity} x {product.name} to your cart.')
        return redirect('menu')

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        return render(request, 'core/cart.html', {'cart': cart, 'step': 1})

    def post(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.cart = cart
            cart_item.save()
            return redirect('confirm_order')
        return render(request, 'core/cart.html', {'cart': cart, 'form': form, 'step': 1})



class ConfirmOrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        return render(request, 'core/confirm_order.html', {'cart': cart, 'step': 2})

    def post(self, request):
        return redirect('choose_delivery')



class ChooseDeliveryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'core/choose_delivery.html', {'step': 3})

    def post(self, request):
        delivery_choice = request.POST.get('delivery_choice')
        if delivery_choice == 'store':
            return redirect('payment')
        elif delivery_choice == 'home':
            return redirect('delivery_address')
        return render(request, 'core/choose_delivery.html', {'step': 3, 'error': 'Please select a delivery method'})


class DeliveryAddressView(LoginRequiredMixin, View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'core/delivery_address.html', {'form': form, 'step': 3})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer
            order.status = 'pending'
            order.save()
            return redirect('payment')
        return render(request, 'core/delivery_address.html', {'form': form, 'step': 3})



class PaymentView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        return render(request, 'core/payment.html', {'cart': cart, 'step': 4})

    def post(self, request):
        cart = get_object_or_404(Cart, customer=request.user.customer)
        order = Order.objects.create(customer=request.user.customer, status='completed')
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        cart.delete()
        return render(request, 'core/order_confirmation.html', {'order': order, 'step': 4})

def order_confirmation(request):
    return render(request, 'core/order_confirmation.html')


class ConfirmOrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        return render(request, 'core/confirm_order.html', {'cart': cart, 'step': 2})

    def post(self, request):
        print("Confirm Order POST request received")
        return redirect('choose_delivery')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, Order
from .forms import ProductForm
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta

# Vistas para la administración personalizada
@staff_member_required
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')

@staff_member_required
def admin_products(request):
    products = Product.objects.all()
    return render(request, 'core/admin_products.html', {'products': products})

from django.db import IntegrityError
@staff_member_required
def admin_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Product created successfully')
                return redirect('admin_products')  # Asegúrate de que esta URL sea correcta
            except IntegrityError:
                messages.error(request, 'Product code must be unique. Please enter a different code.')
    else:
        form = ProductForm()
    return render(request, 'core/admin_product_form.html', {'form': form})


@staff_member_required
def admin_product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/admin_product_form.html', {'form': form})

@staff_member_required
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('admin_products')
    return render(request, 'core/admin_product_confirm_delete.html', {'product': product})

@staff_member_required
def admin_orders(request):
    orders = Order.objects.all()
    return render(request, 'core/admin_orders.html', {'orders': orders})

@staff_member_required
def admin_reports(request):
    return render(request, 'core/admin_reports.html')

@staff_member_required
def report_orders_per_day(request):
    today = timezone.now().date()
    start_date = today - timedelta(days=30)
    orders_per_day = Order.objects.filter(created_at__range=[start_date, today]) \
                                  .annotate(day=TruncDay('created_at')) \
                                  .values('day') \
                                  .annotate(count=Count('id')) \
                                  .order_by('day')
    return render(request, 'core/report_orders_per_day.html', {'orders_per_day': orders_per_day})

@staff_member_required
def report_popular_products(request):
    popular_products = Product.objects.annotate(order_count=Count('orderitem')).order_by('-order_count')[:10]
    return render(request, 'core/report_popular_products.html', {'popular_products': popular_products})

@staff_member_required
def report_orders_per_product(request):
    orders_per_product = Product.objects.annotate(order_count=Count('orderitem')).order_by('-order_count')
    return render(request, 'core/report_orders_per_product.html', {'orders_per_product': orders_per_product})

@staff_member_required
def report_orders_in_period(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        orders_in_period = Order.objects.filter(created_at__range=[start_date, end_date]).count()
        return render(request, 'core/report_orders_in_period.html', {
            'orders_in_period': orders_in_period,
            'start_date': start_date,
            'end_date': end_date
        })
    return render(request, 'core/report_orders_in_period.html')

# Nuevas vistas para la funcionalidad de los domiciliarios
from .forms import DeliveryPersonForm
from .models import DeliveryPerson

@staff_member_required
def list_delivery_persons(request):
    delivery_persons = DeliveryPerson.objects.all()
    return render(request, 'core/list_delivery_persons.html', {'delivery_persons': delivery_persons})

@staff_member_required
def create_delivery_person(request):
    if request.method == 'POST':
        form = DeliveryPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_delivery_persons')
    else:
        form = DeliveryPersonForm()
    return render(request, 'core/delivery_person_form.html', {'form': form})

@staff_member_required
def update_delivery_person(request, pk):
    delivery_person = get_object_or_404(DeliveryPerson, pk=pk)
    if request.method == 'POST':
        form = DeliveryPersonForm(request.POST, instance=delivery_person)
        if form.is_valid():
            form.save()
            return redirect('list_delivery_persons')
    else:
        form = DeliveryPersonForm(instance=delivery_person)
    return render(request, 'core/delivery_person_form.html', {'form': form})

@staff_member_required
def delete_delivery_person(request, pk):
    delivery_person = get_object_or_404(DeliveryPerson, pk=pk)
    if request.method == 'POST':
        delivery_person.delete()
        return redirect('list_delivery_persons')
    return render(request, 'core/delete_delivery_person.html', {'delivery_person': delivery_person})
