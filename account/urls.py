from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import UserLoginForm, PwdResetForm,PwdResetConfirmForm
from . import views

app_name = "account"


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name = "account/login.html", form_class = UserLoginForm, redirect_authenticated_user = True), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>', views.account_activate, name='activate'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_user, name='delete_user'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
                                                         template_name="account/password_reset/password-reset.html",
                                                         success_url = "password-reset-email-confirm",
                                                         email_template_name = "account/password_reset/password-reset-email.html",
                                                         form_class = PwdResetForm), name='password-reset'),
    
    path('password-reset-confirm/<slug:uidb64>/<slug:token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset/password-reset-confirm.html',
        success_url='/account/password-reset/password-reset-complete/',
        form_class=PwdResetConfirmForm),
         name="password-reset-confirm"),
    
    path('password-reset/password-reset-email-confirm/', auth_views.TemplateView.as_view(
        template_name ='account/password_reset/reset-status.html'), name='reset-status-confirmed'),
     
    path('password-reset/password-reset-complete/', auth_views.TemplateView.as_view(
        template_name ='account/password_reset/reset-status.html'), name='reset-status-complete'),
    
    path('addresses/', views.view_addresses, name="addresses"),
    path('add_address/', views.add_address, name="add_address"),
    path('addresses/edit/<slug:id>/', views.edit_address, name="edit_address"),
    path('addresses/delete/<slug:id>/', views.delete_address, name="delete_address"),
    path('addresses/set_default/<slug:id>/', views.set_default, name="set_default"),
    path('wishlist/add/<int:id>/', views.add_to_wishlist, name="add_to_wishlist"),
    path('wishlist/', views.view_wishlist, name="view_wishlist")
    
]
