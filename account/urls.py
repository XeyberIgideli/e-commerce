from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
from . import views
app_name = "account"

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name = "account/login.html", form_class = UserLoginForm, redirect_authenticated_user = True), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>', views.account_activate, name='activate'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    
]
