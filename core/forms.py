from django import forms
from .models import CartItem, Order, Product

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'code'] 

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if Product.objects.filter(code=code).exists():
            raise forms.ValidationError('Product code must be unique. Please enter a different code.')
        return code

from .models import DeliveryPerson

class DeliveryPersonForm(forms.ModelForm):
    class Meta:
        model = DeliveryPerson
        fields = ['name', 'vehicle_type', 'license_number', 'license_expiry', 'availability_hours']