from django.shortcuts import render, get_object_or_404
from .models import Category, Product
# Create your views here.
 
def store_index(request): 
    products = Product.objects.prefetch_related("product_image").filter(is_active = True)
    return render(request, 'store/index.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active = True)
    return render(request, 'store/products/single.html', {'product': product})

def category_detail(request, slug = None):
    category = get_object_or_404(Category, slug=slug) 
    products = Product.objects.filter(category__in = Category.objects.get(name = slug.capitalize()).get_descendants(include_self=True))
    return render(request, 'store/products/category.html', {'category': category, 'products': products})