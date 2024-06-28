from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path('', views.payment_index, name="payment_index"),
    path('add/', views.add_payment, name="add_payment"),
    path('order_succeeded/', views.order_succeeded, name="order-succeeded")
]
