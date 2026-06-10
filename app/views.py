from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .forms import RegisterForm,Identify
from .models import User,UsersModel,ProductItem, product_category,SizeOption,OrderItem, Product,OrderItem, Order,SizeCategory,SizeOption,ProductVariation
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm,PasswordChangeForm,PasswordResetForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
import logging


# @login_required(login_url='login/')
# def add_to_cart(request,productitemslug,sizeslug):
#     username = request.user
#     user = UsersModel.objects.get(username=username)
#     productitem = ProductItem.objects.get(slug = productitemslug)
#     sizeoption = SizeOption.objects.get(slug = sizeslug)

#     OrderItem.objects.create(user = user,productitem=productitem,size=sizeoption)
#     return HttpResponse('Product added to cart successfully')

# @login_required(login_url='login/')
# def add_to_cart(request, productitemslug, sizeslug):
#     try:
#         user = UsersModel.objects.get(user=request.user)
#     except UsersModel.DoesNotExist:
#         return HttpResponse('User not found in UsersModel.', status=404)

#     productitem = get_object_or_404(ProductItem, slug=productitemslug)
#     sizeoption = get_object_or_404(SizeOption, slug=sizeslug)

#     OrderItem.objects.create(user=user, productitem=productitem, size=sizeoption)
#     return HttpResponse('Product added to cart successfully')

@login_required(login_url='login/')
def add_to_cart(request, productitemslug, sizeslug):
    user = get_object_or_404(UsersModel, user=request.user)
    productitem = get_object_or_404(ProductItem, slug=productitemslug)
    sizeoption = get_object_or_404(SizeOption, slug=sizeslug)

    existing_order_item = OrderItem.objects.filter(user=user, productitem=productitem, size=sizeoption).first()

    if existing_order_item:
        if existing_order_item.quantity < sizeoption.qty_in_stock:
            existing_order_item.quantity += 1
            existing_order_item.save()
            return HttpResponse('Product quantity incremented successfully')
        else:
            return HttpResponse('Product out of stock')
    else:
        if sizeoption.qty_in_stock > 0:
            OrderItem.objects.create(user=user, productitem=productitem, size=sizeoption, quantity=1)
            return HttpResponse('Product added to cart successfully')
        else:
            return HttpResponse('Product out of stock')


def increment_quantity(request, id):
    orderitem = get_object_or_404(OrderItem, id=id)
    productitem = get_object_or_404(ProductItem, slug=orderitem.productitem.slug)
    size = get_object_or_404(SizeOption, slug=orderitem.size.slug)
    product_variation = get_object_or_404(ProductVariation, product_item=productitem, size=size)

    if orderitem.quantity < product_variation.qty_in_stock:
        orderitem.quantity += 1
        orderitem.save()
        return HttpResponse('Quantity incremented successfully')
    return HttpResponse('Product out of stock')


def decrement_quantity(request, id):
    orderitem = get_object_or_404(OrderItem, id=id)
    
    if orderitem.quantity > 1:
        orderitem.quantity -= 1
        orderitem.save()
        return HttpResponse('Quantity decremented successfully')
    else:
        orderitem.delete()
        return HttpResponse('Order item removed as quantity was 1')

def baseView(request):
    return render(request, 'base.html')

def signup(request):
    fm = RegisterForm()
    if request.method == 'POST':
        fm = RegisterForm(data=request.POST)
        if fm.is_valid():
            user = fm.save()
            send_mail(
                'Registration Successful',
                f'Hi {user.username}, welcome! Your account has been created successfully.',
                'raghukumarappa2002@gmail.com',
                [user.email]
            )
            return redirect('login')
    return render(request, 'authentication/register.html', {'form': fm})



def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user_model = UsersModel.objects.get(username=username)
            # Manually check the password
            if user_model.password_hash == password:
                # Get the corresponding User instance
                user = user_model.user
                auth_login(request, user)
                send_mail(
                    'Login Successful',
                    f'Hi {username}, you have logged in successfully.',
                    'raghukumarappa2002@gmail.com',
                    [user.email]
                )
                return redirect('home')  # Redirect to home view after successful login
            else:
                return HttpResponse('Invalid password')
        except UsersModel.DoesNotExist:
            return HttpResponse('Invalid username')
            
    return render(request, 'authentication/login.html')

# def loginView(request):
#     fm = AuthenticationForm()
#     if request.method == 'POST':
#         fm = AuthenticationForm(data=request.POST)
#         if fm.is_valid():
#             username = fm.cleaned_data['username']
#             password = fm.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 send_mail(
#                     'Login Successful',
#                     f'Hi {username}, you have logged in successfully.',
#                     'raghukumarappa2002@gmail.com',
#                     [user.email]
#                 )
#                 return redirect('home')  # Redirect to home view after successful login
#             return HttpResponse('Invalid password')
#     return render(request, 'authentication/login.html', {'form': fm})

@login_required 
def home(request): 
    return render(request, 'home.html')

def logoutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login/')
def updatePassword(request):
    username = request.user
    user = UsersModel.objects.get(username=username)
    fm = PasswordChangeForm(user)
    if request.method == 'POST':
        fm = PasswordChangeForm(user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Password updated successfully")
            send_mail(
                'Password Updated',
                f'Hi {username}, your password has been updated successfully.',
                'raghukumarappa2002@gmail.com',
                [user.email]
            )
            return redirect('home')  # Redirect to home or another appropriate page
        else:
            messages.error(request, "Invalid Password")
    return render(request, 'authentication/update.html', {'form': fm})

def identifyView(request):
    fm = Identify()
    if request.method == 'POST':
        fm = Identify(request.POST)
        if fm.is_valid():
            Uname = fm.cleaned_data['username']
            if UsersModel.objects.filter(username=Uname).exists():
                url = '/reset/' + Uname + '/'
                send_mail(
                    'Password Reset Requested',
                    f'Hi {Uname}, a password reset request has been initiated. Please follow the instructions to reset your password.',
                    'raghukumarappa2002@gmail.com',
                    [UsersModel.objects.get(username=Uname).email]
                )
                return redirect(url)
        messages.error(request, 'Invalid username')
    return render(request, 'authentication/identify.html', {'form': fm})

def setPassword(request, username):
    user = UsersModel.objects.get(username=username)
    fm = SetPasswordForm(user)
    if request.method == 'POST':
        fm = SetPasswordForm(user, data=request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "Password reset successful")
            send_mail(
                'Password Reset Successful',
                f'Hi {username}, your password has been reset successfully.',
                'raghukumarappa2002@gmail.com',
                [user.email]
            )
            return redirect("login")
        else:
            messages.error(request, 'Invalid password')
    return render(request, 'authentication/reset.html', {'form': fm})

# def product(request):
#     products = ProductItem.objects.all()
#     return render(request, 'products/products.html', {'products': products })


def product(request):
    products = ProductItem.objects.prefetch_related('size_options').all()
    return render(request, 'products/products.html', {'products': products})

    
def productview(request,slug):
    if ProductItem.objects.filter(slug=slug).exists():
        product=ProductItem.objects.get(slug=slug)
        context={
            'product':product
        }
        return render(request,'products/product_details.html',context)
    return HttpResponse('product does not exist')


# def cat(request,slug):
#     if product_category.objects.filter(slug=slug).exists():
#         category=product_category.objects.get(slug=slug)

#         products = Product.objects.filter(product__category__exact = category)
#         product_items = ProductItem.objects.filter(Product__in = products)
#         return render(request, 'products/category_list.html', {'products': product_items})
#     return HttpResponse("Invalid Category")


def cat(request, slug):
    category = get_object_or_404(product_category, slug=slug)
    products = Product.objects.filter(product_category=category)
    product_items = ProductItem.objects.filter(product__in=products)
    return render(request, 'products/category_list.html', {'products': product_items})



def homeView(request):
    categories = product_category.objects.filter(category_name__in=['Mens-Clothing', 'Womens-Clothing', 'Kids-Clothing'])
    return render(request, 'products/product_list.html', {'categories': categories})


# def category_list(request):
#     categories = product_category.objects.all()
#     return render(request, 'products/category_list.html', {'categories': categories})

# # View to display products by category
# def product_list(request, slug):
#     category = get_object_or_404(product_category, slug=slug)
#     products = Product.objects.filter(product_category=category)
#     return render(request, 'products/product_list.html', {'category': category, 'products': products})







# def productView(request, slug):
#     try:
#         product = ProductItem.objects.get(slug=slug)
#         return render(request, 'products/products.html', {'product': product})
#     except ProductItem.DoesNotExist:
#         return HttpResponse('Product does not exist', status=404)


# def productView(request,id):
#     if ProductItem.objects.filter(product_item_id=id).exists():
#         products=ProductItem.objects.get(product_item_id=id)
#         return render(request, 'products/products.html', {'products': products })
#     return HttpResponse('Product does not exist')

    # def productView(request, id):
    #     try:
    #         product = ProductItem.objects.get(product_item_id=id)
    #         return render(request, 'products/products.html', {'product': product })
    #     except ProductItem.DoesNotExist:
    #         return HttpResponse('Product does not exist')

    

