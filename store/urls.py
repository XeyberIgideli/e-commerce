from django.urls import path 
from . import views

app_name = 'store' 

urlpatterns = [
    path('', views.store_index, name='store_index'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('category/<slug:slug>', views.category_detail, name='category_detail'),
]
 