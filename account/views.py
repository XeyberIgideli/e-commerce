from django.shortcuts import redirect, render

from account.models import UserBase
from .forms import RegistrationForm
from .token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
# Create your views here.

def register (request):
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
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = UserBase.objects.get(pk=uid) 
        
        if user is not None and account_activation_token.check_token(token):
            user.is_active = True
            user.save()
            # login(request,  user)
            
    except:
        pass
