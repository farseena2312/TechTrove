
from django.apps import apps
from django.contrib import admin
from user_homepage.models import Category, Product

# Register your models here.

app_models = apps.get_app_config('admin_account').get_models()
for model in app_models:
    try:    

        admin.site.register(model)

    except Exception:
        pass



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'slug', 'description', 'actual_price', 'product_offer', 'offer', 'offer_price',  'product_image1', 'product_image2', 'product_image3', 'stock', 'is_available', 'category')

    list_filter = ( 'category',)

    def save_model(self, request, obj, form, change):
        # Customize save behavior if needed
        obj.save()

