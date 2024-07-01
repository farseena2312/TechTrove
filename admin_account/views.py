
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from user_homepage.models import Category, Product, Variation
from order.models import Order, OrderProduct
from .forms import CategoryForm, ProductForm, UserForm, VariationForm, OrderForm, OrderProductForm
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, authenticate
from .forms import LoginForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .forms import ProductForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()


@never_cache
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('admin_index')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'admin_account/admin_login.html', {'form': form})


@login_required
@never_cache

def logout_view(request):
    logout(request)
    return redirect('admin_login')


def admin_index(request):
  return render(request, "admin_account/admin_index.html")



# ----product----#

# # # @login_required(login_url='admin_login')

def product(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(product_name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'admin_account/pages/product_list.html', {'products': products})


def edit_product(request, product_slug):
    # Retrieve the product object
    product = get_object_or_404(Product, slug=product_slug)
    
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            # Save the updated data to the database
            form.save()
            # Redirect to a success page or product detail page
            return redirect('product')  
    else:
        # Populate the form with current product data for editing
        form = ProductForm(instance=product)
    
    # Render the edit product template with the form
    return render(request, 'admin_account/pages/edit_product.html', {'form': form, 'product': product})


def activate_inactivate_product(request, product_slug):
    # Retrieve the product object based on product_slug
    product = get_object_or_404(Product, slug=product_slug)
    
    # Toggle product availability
    if product.is_available:
        # If product is available, set it to unavailable (block)
        product.is_available = False
        action = 'blocked'
    else:
        # If product is unavailable, set it to available (unblock)
        product.is_available = True
        action = 'unblocked'
    
    # Save the updated product instance
    product.save()
    
    # Return a response indicating the action taken
    return HttpResponse(f'Product {product_slug} {action} successfully.')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('product')  # Redirect to the product list page
    else:
        form = ProductForm()

    return render(request, 'admin_account/pages/add_product.html', {'form': form})    


def activate_inactivate_product(request, product_slug):
    # Retrieve the product object based on product_slug
    product = get_object_or_404(Product, slug=product_slug)
    
    # Toggle product availability
    if product.is_available:
        # If product is available, set it to unavailable (block)
        product.is_available = False
        action = 'blocked'
    else:
        # If product is unavailable, set it to available (unblock)
        product.is_available = True
        action = 'unblocked'
    
    # Save the updated product instance
    product.save()
    
    # Return a response indicating the action taken
    return HttpResponse(f'Product {product_slug} {action} successfully.')
    return render(request, 'admin_account/pages/add_product.html', {'form': form})


def save_product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Saves the form data to the database
            return redirect('product')  # Redirects to the product list page
    else:
        form = ProductForm()
    
    return render(request, 'admin_account/pages/add_product.html', {'form': form})    


def save_product_edit(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product', product_slug=product.slug)  # Redirect to product detail page
    else:
        # Handle GET request if needed
        pass
    
    # Redirect or render a different template if needed
    return redirect('admin_account/pages/edit_product.html', product_slug=product.slug)


# -----category-----#

def category(request):
    query = request.GET.get('q')
    if query:
        category = Category.objects.filter(category_name__icontains=query)
    else:
        category = Category.objects.all()

    return render(request, 'admin_account/pages/category.html', {'category': category})


def edit_category(request, category_slug):
    # Retrieve the category object
    category = get_object_or_404(Category, slug=category_slug)
    
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            # Save the updated data to the database
            form.save()
            # Redirect to a success page or category detail page
            return redirect('category')  
    else:
        # Populate the form with current category data for editing
        form = CategoryForm(instance=category)
    
    # Render the edit category template with the form
    return render(request, 'admin_account/pages/edit_category.html', {'form': form, 'category': category})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category')  # Redirect to the category list view after successful form submission
    else:
        form = CategoryForm()

    return render(request, 'admin_account/pages/add_category.html', {'form': form})     


def save_category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Saves the form data to the database
            return redirect('category')  # Redirects to the category list page
    else:
        form = CategoryForm()
    
    return render(request, 'admin_account/pages/add_category.html', {'form': form})    


def save_category_edit(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    
    if request.method == 'POST':
        form = CategorytForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category', category_slug=category.slug)  # Redirect to category detail page
    else:
        # Handle GET request if needed
        pass
    
    # Redirect or render a different template if needed
    return redirect('admin_account/pages/edit_category.html', category_slug=category.slug)



@login_required(login_url='admin_login')          
def variations(request):
    query=request.GET.get('q')
    if query:
        variations=Variation.objects.filter(Q(product__product_name__icontains=query) | Q(variation_category__icontains=query) | Q(variation_value__icontains=query))
    else:
        variations=Variation.objects.all()
    
    paginator=Paginator(variations, 10)
    page=request.GET.get('page')
    try:
        paged_variations=paginator.get_page(page)
    except PageNotAnInteger:
        paged_variations = paginator.page(1)
    except EmptyPage:
        paged_variations = paginator.page(paginator.num_pages)
    context={
        'variations':paged_variations,
        'query':query,
    }
    return render(request,'admin_account/pages/variations.html', context)





@login_required(login_url='admin_login') 
def add_variation(request):
    if request.method=='POST':
        product_id=request.POST['product']
        variation_category=request.POST['variation_category']
        variation_value=request.POST['variation_value']
        variation_exists=Variation.objects.filter(product_id=product_id,variation_category__iexact=variation_category,variation_value__iexact=variation_value).exists()
        if variation_exists:
            messages.error(request,'Variation already exists')
            return redirect('add-variation')
        product=get_object_or_404(Product, id=product_id)
        variation=Variation.objects.create(product=product,variation_category=variation_category,variation_value=variation_value)
        variation.save()
        return redirect('variations')
    else:
        products=Product.objects.all()
        variations_categories=Variation.variation_category_choice
        context={
            'products':products,
            'variations_categories':variations_categories,
        }
        return render(request,'admin_account/pages/add_variation.html',context)




@login_required(login_url='admin_login')   
def edit_variation(request, variation_id):
    variation=Variation.objects.get(id=variation_id)
    if request.method=='POST':
        product_id=request.POST['product']
        variation_category=request.POST['variation_category']
        variation_value=request.POST['variation_value']
        variation_exists=Variation.objects.filter(product_id=product_id,variation_category__iexact=variation_category,variation_value__iexact=variation_value).exists()
        if variation_exists:
            messages.error(request,'Variation already exists')
            return redirect('edit_variation', variation_id=variation.id)
        product=get_object_or_404(Product, id=product_id)
        variation.product=product
        variation.variation_category=variation_category
        variation.variation_value=variation_value
        variation.save()
        return redirect('variations')
    else:
        products=Product.objects.exclude(id=variation.product.id)
        variations_categories=Variation.objects.values('variation_category').distinct()
        context={
            'products':products,
            'variation':variation,
            'variations_categories':variations_categories,
        }
        return render(request,'admin_account/pages/edit_variation.html',context)  



@login_required(login_url='login')  
def activate_inactivate_variation(request, variation_id):
    variation=Variation.objects.get(id=variation_id)
    if variation.is_active:
        variation.is_active=False
    else:
        variation.is_active=True
    variation.save()
    return redirect('variations')                      




# ------user_list------#     

def admin_users(request):
    if not request.user.is_superuser:
        return redirect('admin_login')  # Redirect if not superuser
    
    users = User.objects.filter(is_staff=True)  # Filter users who are staff/admin
    return render(request, 'admin_account/pages/user.html', {'users': users})

def block_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('admin_login')  # Redirect if not superuser
    
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_users')

def unblock_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('admin_login')  # Redirect if not superuser
    
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_users')



# ----------order-----------#

@login_required(login_url='admin_login')   

def orders(request):
    query=request.GET.get('q')
    if query:
        orders=Order.objects.filter(
            Q(order_number__icontains=query) | 
            Q(user__username__icontains=query) | 
            Q(status__icontains=query) | 
            Q(payment__payment_method__icontains=query),
            is_ordered=True,
        ).exclude(status='New').order_by('-created_at')
    else:
        orders=Order.objects.filter(is_ordered=True).exclude(status='New').order_by('-created_at')
    
    paginator=Paginator(orders, 10)
    page=request.GET.get('page')
    try:
        paged_orders=paginator.get_page(page)
    except PageNotAnInteger:
        paged_orders = paginator.page(1)
    except EmptyPage:
        paged_orders = paginator.page(paginator.num_pages)
    context={
        'orders':paged_orders,
        'query': query,
    }
    return render(request,'admin_account/orders.html', context)



@login_required(login_url='admin_login') 

def orders_detail(request,order_id):
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    
    context={
        'order_detail':order_detail,
        'order':order,
        'discount': order.discount if order.discount else 0
    }
    return render(request,'admin_account/orders_detail.html', context)



@login_required(login_url='admin_login') 

@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            new_status = data.get('status')

            order = Order.objects.get(id=order_id)
            order.status = new_status
            if new_status == 'Delivered' and order.payment.status=='Pending':
                order.payment.status='COMPLETED'
            order.save()
            order.payment.save() 

            return JsonResponse({'success': True, 'new_status': order.get_status_display()})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



