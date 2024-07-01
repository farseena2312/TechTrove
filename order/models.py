from django.db import models

# Create your models here.
from user_account.models import UserAccount
from user_homepage.models import UserAddress, Product, Variation



class Payment(models.Model):
    PAYMENT_METHOD_CHOICES=(
        ('cod','cod'),
    )
    user=models.ForeignKey(UserAccount, on_delete=models.CASCADE, default=0)
    payment_id=models.CharField(max_length=100, default=0)
    payment_method=models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    amount_paid=models.CharField(max_length=100, default=0)
    status=models.CharField(max_length=100)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Ordered','Ordered'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )
    user=models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True)
    order_number=models.CharField(max_length=50)
    payment=models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    address=models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    order_note=models.CharField(max_length=100, blank=True)
    order_total=models.IntegerField()
    delivery_charge=models.IntegerField()
    status=models.CharField(max_length=100,choices=STATUS, default='New')
    ip=models.CharField(blank=True, max_length=200)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.order_number
     

        

class OrderProduct(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    user=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation, blank=True)
    quantity=models.IntegerField()
    product_price=models.IntegerField()
    ordered=models.BooleanField(default=False)
    payment=models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    

