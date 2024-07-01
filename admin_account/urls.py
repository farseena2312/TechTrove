from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_index/', views.admin_index,  name='admin_index'),

    path('product/', views.product, name='product'),
    path('add_product/', views.add_product, name='add-product'),
    path('<slug:product_slug>/activate_inactivate_product', views.activate_inactivate_product, name='activate_inactivate_product'),
    path('edit_product/<slug:product_slug>/', views.edit_product, name='edit_product'),
    path('save-product/', views.save_product_add, name='save_product'),
    path('save_product/<slug:product_slug>/', views.save_product_edit, name='save_product'),
    path('category/', views.category, name='category'),
    path('edit_category/<slug:category_slug>/', views.edit_category, name='edit_category'),
    path('add_category/', views.add_category, name='add-category'),
    path('save-category/', views.save_category_add, name='save_category'),
    path('save_category/<slug:category_slug>/', views.save_category_edit, name='save_category'),
    
    path('variation/', views.variations, name='variations'),
    path('variation/add_variation/', views.add_variation, name='add-variation'),
    path('variation/edit_variation/<int:variation_id>/', views.edit_variation, name='edit_variation'),
    path('activate_inactivate_variation/<int:variation_id>/', views.activate_inactivate_variation, name='activate_inactivate_variation'),

    path('admin_users/', views.admin_users, name='admin_users'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),

     path('orders/', views.orders, name='orders'),
    path('orders_detail/<int:order_id>/', views.orders_detail, name='orders-detail'),
    path('update_status/', views.update_status, name='update_status'),
    
    
]    