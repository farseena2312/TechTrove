from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place-order'),
    path('my_orders/', views.my_orders, name='my-orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order-detail'),
    path('cancel_order/<int:order_number>/', views.cancel_order, name='cancel_order'),
    path('cod_complete/', views.cod_complete, name='cod_complete'),

]    