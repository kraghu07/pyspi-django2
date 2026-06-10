from django.shortcuts import render
from .models import ProductCategory, Product

def category_list(request):
    categories = ProductCategory.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})


def product_list(request, category_slug):
    category = ProductCategory.objects.get(slug=category_slug)
    products = Product.objects.filter(product_category=category)
    return render(request, 'shop/product_list.html', {'category': category, 'products': products})


def product_detail(request, product_slug):
    product = Product.objects.get(slug=product_slug)
    return render(request, 'shop/product_detail.html', {'product': product})
