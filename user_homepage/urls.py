from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='index'),
    path('shop/', views.shop, name='Shop'),
    path('history/', views.history, name='History'),
    path('about/', views.about, name='About'),
    path('contact_us/', views.contact_us, name='Contact_us'),

    path('product/<slug:category_slug>/<slug:product_slug>/', views.productview, name='productview'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'), 

    path('profile_information/', views.profile_information, name='profile-information'),
    
    path('get-address-details/<int:address_id>/', views.get_address_details, name='get-address-details'),
    path('add_new_address/', views.add_new_address, name='add-new-address'),
    path('manage_address/', views.manage_address, name='manage-address'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit-address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('change_password/', views.change_password, name='change_password'),


    path('my_orders/', views.my_orders, name='my-orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order-detail'),
    path('cancel_order/<int:order_number>/', views.cancel_order, name='cancel_order'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),


     path('wishlist/', views.wishlist, name='wishlist'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('remove_wishlist/<int:product_id>/', views.remove_wishlist, name='remove_wishlist'),
    
]
