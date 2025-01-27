import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DeliveryOptions
# Create your views here.

@login_required
def delivery_choices (request):
    options = DeliveryOptions.objects.filter(is_active = True)
    return render(request, 'checkout/delivery_choices.html', {"deliveryoptions": options})

@login_required
def update_delivery_choices (request):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        delivery_id = post_data["delivery_id"]
    
    return JsonResponse(data={"test": 123})