from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from account.models import UserBase
from .forms import RegistrationForm,EditForm
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@login_required
def dashboard (request):
    return render(request, 'account/dashboard/index.html')

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
    user = UserBase.objects.get(id = request.user.id)  
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
        user = UserBase.objects.get(pk=uid)  
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request,  user)
            return redirect("account:dashboard")
        else:
            return render(request,"account/register/invalid-confirmation.html") 
            
