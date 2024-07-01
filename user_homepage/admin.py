from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import Useradmin
from .models import Category, Product, ReviewRating, WishList, Variation

 
# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(ProductImage)
admin.site.register(ReviewRating)
admin.site.register(WishList)
admin.site.register(Variation)
