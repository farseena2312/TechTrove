from django.shortcuts import render, redirect
from cart.models import CartItem
from user_homepage.models import UserAddress
from . models import Order, OrderProduct, Payment
from  user_homepage.models import Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import time
from django.shortcuts import get_object_or_404
from django.contrib import messages


# Create your views here.



@login_required(login_url='login')

def my_orders(request):
    query=request.GET.get('q')
    if query:
        ordered_product=OrderProduct.objects.filter(
            Q(product__product_name__icontains=query) |
            Q(order__status__icontains=query),
            user=request.user, 
            ordered=True
        ).order_by('-created_at')
    else:
        ordered_product=OrderProduct.objects.filter(user=request.user, ordered=True).order_by('-created_at')
        print("Ordered Product:", ordered_product)
    
    print(ordered_product)
    grouped_orders = {}
    for product in ordered_product:
        order_number=product.order.order_number
        if order_number not in grouped_orders:
            grouped_orders[order_number]=[]
        grouped_orders[order_number].append(product)
    context={
        'ordered_product':ordered_product,
        'grouped_orders':grouped_orders,
    }
    return render(request,'orders/my_orders.html', context)



@login_required(login_url='login')

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('Shop')

    grand_total = 0
    delivery_charge = 0

    for cart_item in cart_items:
        if not cart_item.product.is_available or cart_item.product.stock <= 0:
            cart_item.is_active = False
            cart_item.save()
        else:
            total += (cart_item.product.offer_price * cart_item.quantity)
            quantity += cart_item.quantity

    cart_items = CartItem.objects.filter(user=current_user, is_active=True).select_related('product')

    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('Shop')

    if total < 500 and total != 0:
        delivery_charge = 50

    grand_total = total + delivery_charge

   

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'cod')  # Default to COD
        selected_address_id = request.POST.get('address_id')
        order_note = request.POST.get('order_note')
        ip = request.META.get('REMOTE_ADDR')

        if selected_address_id:
            try:
                selected_address = UserAddress.objects.get(id=selected_address_id)
            except UserAddress.DoesNotExist:
                return redirect('checkout')
        else:
            selected_address = UserAddress(
                user=request.user,
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                phone_number=request.POST['phone_number'],
                email=request.POST['email'],
                address_line1=request.POST['address_line1'],
                address_line2=request.POST['address_line2'],
                country=request.POST['country'],
                state=request.POST['state'],
                city=request.POST['city'],
                zip_code=request.POST['zip_code'],
            )
            selected_address.save()

        order = Order(
            user=request.user,
            address=selected_address,
            order_note=order_note,
            order_total=grand_total,
            delivery_charge=delivery_charge,
            ip=ip,
        )
        order.save()
        timestamp = int(time.time() * 1000)  
        order_number = f'{timestamp}{order.id}'
        order.order_number = order_number
        order.save()

        order_products = []
        for cart_item in cart_items:
            if cart_item.product.is_available and cart_item.product.stock > 0:
                order_products.append(OrderProduct(
                    order=order,
                    user=request.user,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    product_price=cart_item.product.offer_price,
                    ordered=True
                ))

        OrderProduct.objects.bulk_create(order_products)


        request.session['order_number'] = order_number

        if payment_method == 'cod':
            order.is_ordered = True
            order.save()
            return redirect('cod_complete')  # Redirect to a completion page

    else:
        return redirect('checkout')




@login_required(login_url='login')

def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = sum(item.product_price * item.quantity for item in order_detail)
    
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'orders/order_detail.html', context)



@login_required(login_url='login')

def cancel_order(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if order.status == 'Delivered':
        messages.error(request, "You cannot cancel an order that has been delivered.")
        return redirect('order-detail', order_id=order_number)
    
    if order.payment:
        if order.payment.payment_method == 'cod':
            messages.info(request, "Cash on delivery orders cannot be refunded automatically.")
        elif order.payment.status == 'COMPLETED':
            order.payment.status = 'REFUNDED'
            order.payment.save()
            messages.success(request, "Your order has been cancelled successfully. Refund process initiated.")
        else:
            messages.info(request, "This order does not have a completed payment record.")
    else:
        messages.info(request, "This order does not have a payment record.")

    order.status = 'Cancelled'
    order.save()

    return redirect('order-detail', order_id=order_number)



def cod_complete(request):
    order_number = request.session.get('order_number')
    
    if not order_number:
        return redirect('Shop')  # Redirect if no order number is found in session

    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    context = {
        'order': order,
    }
    return render(request, 'orders/cod_complete.html', context)