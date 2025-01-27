from django.urls import path
from . import views
app_name = "checkout"

urlpatterns = [
    path("delivery_choices/", views.delivery_choices, name="delivery_choices"),
    path("update_delivery_choices/", views.update_delivery_choices, name="update_delivery_choices"),
    
]
