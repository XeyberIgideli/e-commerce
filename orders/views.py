from django.shortcuts import render
from basket.basket import Basket
from .models import Order,OrderItem
import json
from django.http.response import HttpResponse
# Create your views here.

def add_order (request):
    basket = Basket(request)
    
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        user_id = request.user.id
        order_key = body["order_key"]
        basket_total = basket.get_total_price()
        
        if Order.objects.filter(order_key = order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',
                                address2='add2', total_paid=basket_total, order_key=order_key, billing_status = True)
            order_id = order.pk 
            
            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['quantity'])
    
        return HttpResponse({"success": "Added"})
