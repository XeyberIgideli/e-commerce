from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.urls import reverse
from account.models import Customer,Address
from .forms import RegistrationForm,EditForm, UserAddressForm
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order,Product
# Create your views here.

@login_required
def dashboard (request):
    orders = Order.objects.filter(user=request.user.id).filter(billing_status = True)
    return render(request, 'account/dashboard/index.html', {"orders": orders})

@login_required
def logout_view (request):
    logout(request)
    return redirect("account:login")

@login_required
def edit_profile (request):
    if request.method == "POST":
         edit_form = EditForm(instance = request.user, data = request.POST)   
         if edit_form.is_valid():
             edit_form.save()
    edit_form = EditForm(instance = request.user)    
    return render(request,"account/dashboard/edit-profile.html", {'edit_form': edit_form}) 

@login_required 
def delete_user (request): 
    user = Customer.objects.get(id = request.user.id)  
    user.is_active = False
    user.save()
    logout(request)
    return render(request,"account/dashboard/delete-info.html") 

def password_reset (request):
    pass
 
def register (request):
    referer = request.META.get('HTTP_REFERER') 
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
         
        if registerForm.is_valid():
           user = registerForm.save(commit=False)
           user.email = registerForm.cleaned_data['email']
           user.set_password(registerForm.cleaned_data['password'])
           user.is_active = False
           
           user.save()
           
           current_site = get_current_site(request)
           mail_subject = "Activate your account"
           message = render_to_string("account/register/activation-email.html", {
               'user': user,
               'domain': current_site.domain,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': account_activation_token.make_token(user)
           })
 
           user.send_email(subject = mail_subject, message = message)
           return render(request, 'account/register/register-confirmed.html', {'form': registerForm})
        else:
           return render(request,"account/register/index.html", {'form': registerForm}) 
    else:       
        registerForm = RegistrationForm()
        return render(request,"account/register/index.html", {'form': registerForm}) 
    
    
def account_activate(request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = Customer.objects.get(pk=uid)  
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request,  user)
            return redirect("account:dashboard")
        else:
            return render(request,"account/register/invalid-confirmation.html") 
            

# Addresses
@login_required
def view_addresses (request):
    addresses = Address.objects.filter(customer=request.user)
    
    return render (request, 'account/dashboard/addresses.html', {"addresses": addresses})

@login_required
def add_address (request):
    if request.method == "POST":
        address_form = UserAddressForm(data = request.POST) 
        if address_form.is_valid():
           address_form = address_form.save(commit=False) 
           address_form.customer = request.user
           address_form.save()
           return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm() 
    return render (request, 'account/dashboard/edit_addresses.html', {"form": address_form})

@login_required
def edit_address (request, id):
    if request.method == "POST":
        address = Address.objects.get(pk = id, customer = request.user)
        address_form = UserAddressForm(instance = address, data = request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk = id, customer = request.user)
        address_form = UserAddressForm(instance = address) 
    return render(request, "account/dashboard/edit_addresses.html",{"form": address_form, "method": "patch"})

@login_required
def delete_address (request, id):
    Address.objects.get(pk=id, customer = request.user).delete()
    return redirect("account:addresses") 

@login_required 
def set_default (request, id):
    Address.objects.filter(customer = request.user, default = True).update(default = False)
    Address.objects.filter(pk = id, customer = request.user).update(default = True)
    return redirect("account:addresses")

@login_required
def add_to_wishlist (request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id = request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.error(request, product.title + "has been removed from wishlist.")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + "to your wishlist.")
        
    return HttpResponseRedirect(request.META["HTTP_REFERER"])    

@login_required
def view_wishlist (request):
    products = Product.objects.filter(users_wishlist = request.user)
    return render(request, "account/dashboard/wishlist.html",{"wishlist": products})

            