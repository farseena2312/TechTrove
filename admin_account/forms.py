from django import forms
from user_homepage.models import Category, Product, Variation
from order.models import Order, OrderProduct
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['slug', 'name', 'image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'slug', 'description', 'actual_price', 'product_offer', 'offer', 'offer_price',  'product_image1', 'product_image2', 'product_image3', 'stock', 'is_available', 'category']



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product', 'variation_category', 'variation_value']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'order_number', 'address', 'order_note', 'order_total', 'delivery_charge', 'status']   


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['order', 'user', 'product', 'variations', 'quantity', 'product_price', 'ordered']                