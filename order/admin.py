from django.contrib import admin

# Register your models here.
from . models import Order,OrderProduct


class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    extra=0

class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderProductInline]

admin.site.register(Order)
admin.site.register(OrderProduct)
