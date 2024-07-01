from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from user_account.models import UserAccount
from cart.models import CartItem, Cart
from order.models import Order, OrderProduct
from cart.views import _cart_id, add_cart, remove_cart_item, cart
from order.views import  my_orders, place_order, order_detail, cancel_order
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.http import JsonResponse
from .models import Category, Product, ReviewRating,  WishList, Variation   
from .models import UserProfile,  UserAddress
import logging
from . forms import ReviewForm
from .forms import UserForm, UserProfileForm
from django.db.models import Q



def homepage(request):
    print(">>>>>", request.user)
    categories = Category.objects.filter(status=0)
    products = Product.objects.filter(category__in=categories)
    return render(request, 'homepage_inc/index.html', {"categories": categories, "products": products})



def shop(request):
    categories = Category.objects.filter(status=0)
    products = Product.objects.filter(category__in=categories)
    return render(request, 'homepage_inc/shop.html', {"categories": categories, "products": products})


def history(request):
    # Implement your dashboard logic here
    return render(request, 'homepage_inc/shop.html')


def about(request):
    # Implement your dashboard logic here
    return render(request, 'homepage_inc/shop.html')


def contact_us(request):
    # Implement your dashboard logic here
    return render(request, 'homepage_inc/shop.html')




def productview(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    context = {
        'product': product,
    }
    return render(request, 'homepage_inc/productview.html', context)




@login_required(login_url='login')
def submit_review(request,product_id):
    url=request.META.get('HTTP_REFERER') #store the previous url
    if request.method=='POST':
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form=ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request,"Thank You! Your review has been updated successfully")
            return redirect(url)
        except ReviewRating.DoesNotExist: 
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get("REMOTE_ADDR")
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,"Thank You! Your review submitted")
                return redirect(url)




@login_required(login_url='login')
def profile_information(request):
    user=request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method=='POST':
        user_form=UserForm(request.POST, instance=user)
        profile_form=UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated')
            return redirect('profile-information')
    else:
        user_form=UserForm(instance=user)
        profile_form=UserProfileForm(instance=user_profile)
    return render(request,'homepage_inc/profile.html',{'user_form':user_form,'profile_form':profile_form})


@login_required(login_url='login')

def get_address_details(request, address_id):
    try:
        address = UserAddress.objects.get(id=address_id)
        data = {
            'first_name': address.first_name,
            'last_name': address.last_name,
            'email': address.email,
            'phone_number': address.phone_number,
            'address_line1': address.address_line1,
            'address_line2': address.address_line2,
            'country': address.country,
            'state': address.state,
            'city': address.city,
            'zip_code': address.zip_code,
        }
        return JsonResponse(data)
    except UserAddress.DoesNotExist:
        return JsonResponse({'error': 'Address not found'}, status=404)


@login_required(login_url='login')

def add_new_address(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone_number=request.POST['phone_number']
        email=request.POST['email']
        address_line1=request.POST['address_line1']
        address_line2=request.POST['address_line2']
        country=request.POST['country']
        state=request.POST['state']
        city=request.POST['city']
        zip_code=request.POST['zip_code']

        # Set all existing addresses to not default
        UserAddress.objects.filter(user=request.user, is_deleted=False).update(is_default=False)

        new_address=UserAddress(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            address_line1=address_line1,
            address_line2=address_line2,
            country=country,
            state=state,
            city=city,
            zip_code=zip_code,
            is_default=True
            )
        new_address.save()
        return redirect('manage-address')
    else:
        pass


def manage_address(request):
    addresses=UserAddress.objects.filter(user=request.user, is_deleted=False).order_by('-created_at')
    context={
        'addresses':addresses
    }
    return render(request,'homepage_inc/manage_address.html', context)     



@login_required(login_url='login')  
def edit_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id)
    if request.method== 'POST':
        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.email = request.POST.get('email')
        address.phone_number = request.POST.get('phone_number')
        address.address_line1 = request.POST.get('address_line1')
        address.address_line2 = request.POST.get('address_line2')
        address.country = request.POST.get('country')
        address.state = request.POST.get('state')
        address.city = request.POST.get('city')
        address.zip_code = request.POST.get('zip_code')

        address.save()
        return redirect('manage-address') 

    return render(request,'homepage_inc/manage_address.html',{'address':address})


@login_required(login_url='login')

def change_password(request):
    user=request.user
    if request.method=='POST':
        old_password=request.POST['old_password']
        new_password=request.POST['new_password']
        retype_password=request.POST['retype_password']
        if check_password(old_password, user.password):
            if new_password != retype_password:
                messages.error(request,"Password do not match")
                return render(request,'homepage_inc/change_password.html')
            elif check_password(new_password, user.password):
                messages.error(request,"Please enter a new password")
                return render(request,'homepage_inc/change_password.html')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request,"Password changed successfully")
                return render(request,'homepage_inc/change_password.html')
        else:
            messages.error(request,"Entered password does not match with your account password")
            return render(request,'homepage_inc/change_password.html')
    else:
        return render(request,'homepage_inc/change_password.html')    



@login_required(login_url='login')
def delete_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id)
    address.is_deleted=True
    address.save()
    return redirect('manage-address')       



@login_required(login_url='login')

def wishlist(request):
    wishlist = WishList.objects.filter(user=request.user)
    context={
        'wishlist':wishlist
    }
    return render(request,'homepage_inc/wishlist.html', context)



@login_required(login_url='login')

def add_wishlist(request):
    pid=request.GET['product']
    product=Product.objects.get(id=pid)
    data={}
    check_wishlist=WishList.objects.filter(product=product,user=request.user).count()
    if check_wishlist > 0:
        data={
            'bool':False
        }
    else:
        wishlist=WishList.objects.create(product=product,user=request.user)
        data={
            'bool':True
        }
    return JsonResponse(data)



@login_required(login_url='login')

def remove_wishlist(request, product_id):
    wishlist_item=get_object_or_404(WishList, user=request.user, product_id=product_id)
    wishlist_item.delete()
    return redirect('wishlist')