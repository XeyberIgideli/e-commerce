from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_index, name='basket_index'),
    path('add_basket/', views.add_basket, name='add_basket'),
]
