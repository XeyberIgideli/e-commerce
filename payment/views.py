import os

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from basket.basket import Basket
import stripe
# Create your views here.

@login_required
def payment_index (request):
    basket = Basket(request)
    # print([bask for bask in basket])
    totalModified = str(basket.get_total_price()).replace('.', '')
    total = int(totalModified)  
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    intent = stripe.PaymentIntent.create(
        amount = total,
        currency = 'usd',
        metadata = {"user_id": request.user.id}
    )  
    return render(request, "payment/payment-form.html", {"client_secret": intent.client_secret, 
                                                         "STRIPE_PUBLISHABLE_KEY": os.getenv("STRIPE_PUBLISHABLE_KEY")})

@login_required
def add_payment (request):
    pass

@login_required
def order_succeeded (request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/order-succeeded.html')