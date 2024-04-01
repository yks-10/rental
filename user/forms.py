from django.forms import ModelForm
from .models import User, Product, Order

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'name', 'email', 'password']

class ProductForm(ModelForm):
    class Meta:
        model = Product 
        fields = ['product_name', 'price', 'quantity', 'available']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = []

