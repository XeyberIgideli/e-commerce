from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .basket import Basket
from store.models import Product
import json
# Create your views here.

def basket_index (request):
    basket = Basket(request)
    return render(request, 'store/basket/index.html', {"basket": basket})

def add_basket (request):
    basket = Basket(request)
    if request.method == 'POST':
      post_data = json.loads(request.body.decode("utf-8"))
      product_id = int(post_data['product_id'])
      product_quantity = int(post_data['product_quantity'])  
      product = get_object_or_404(Product, id = product_id)  
      basket.add(product = product, product_quantity = product_quantity)
      
      basket_quantity = basket.__len__() 
      return JsonResponse({"quantity": basket_quantity}) 
   