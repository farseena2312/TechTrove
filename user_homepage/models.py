
from django.db import models
from user_account.models import UserAccount
from django.conf import settings
import uuid
from django.template.defaultfilters import slugify
import random
import string
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Avg,Count



UserAccount = get_user_model()


class Category(models.Model):
    slug = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to="images", null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default,1=Hidden")

    def __str__(self):
        return self.name



class Product(models.Model):
    product_name=models.CharField(max_length=100, default='default_name')
    slug=models.SlugField(max_length=100, unique=True)
    description=models.TextField(max_length=500, blank=True)
    actual_price=models.IntegerField(default=0)
    product_offer=models.FloatField(default=0, null=True, blank=True)
    offer=models.IntegerField(default=0)
    offer_price=models.IntegerField(default=0)
    product_image1=models.ImageField(upload_to='photos/products')
    product_image2=models.ImageField(upload_to='photos/products')
    product_image3=models.ImageField(upload_to='photos/products')
    stock=models.IntegerField(default=0)
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at=models.DateTimeField(default=timezone.now, editable=False)
    updated_at=models.DateTimeField(auto_now=True)
    def get_url(self):
        return reverse('productview', args=[self.category.slug, self.slug])


    def average_review(self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg

        
    
    def count_review(self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count=int(reviews['count'])
        return count

    
class ReviewRating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100, blank=True)
    review=models.TextField(max_length=500,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=20, blank=True)
    status=models.BooleanField(default=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
       

    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class VariationManager(models.Manager):
    def colors(self):
        return self.filter(variation_category='color', is_active=True)
    def sizes(self):
        return self.filter(variation_category='size', is_active=True)

class Variation(models.Model):
    variation_category_choice=(
    ('color','color'),
    ('size','size'),
)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)  
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    objects=VariationManager()

    def __str__(self):
        return self.variation_category + ' ' + self.variation_value + ' ' + self.product.product_name





class UserProfile(models.Model):
    GENDER_CHOICES=[
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    ]
    user=models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='photos/profile_pictures', blank=True, null=True)
    date_of_birth=models.DateField(blank=True, null=True)
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    referral_code = models.CharField(max_length=12, unique=True, blank=True, null=True)
    referred_by=models.ForeignKey(UserAccount, on_delete=models.SET_NULL, related_name='referrals', null=True, blank=True)


    def __str__(self):
        return self.user.first_name



class UserAddress(models.Model):
    user=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100,blank=True, null=True)
    email=models.EmailField(max_length=100)
    phone_number=models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True, null=True)
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_deleted=models.BooleanField(default=False)
    is_default=models.BooleanField(default=False)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line1} {self.address_line2}'
    def __str__(self):
        return self.first_name



class WishList(models.Model):
    user=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)   