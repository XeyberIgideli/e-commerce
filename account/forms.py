from django import forms
from django.contrib.auth.forms import AuthenticationForm

from account.models import UserBase


class UserLoginForm (AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mb-3", "placeholder": "Username", "id": "login-username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control ", "placeholder": "Password", "id": "login-password"}))
    

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserBase
        fields = ('email', 'username',)

    email = forms.EmailField(required=True, max_length=100,help_text='Enter valid email', error_messages={'required': 'Enter valid email'})
    username = forms.CharField(required=True, label='Username', help_text='Username must be unique', min_length=4, max_length=50)
    password = forms.CharField(required=True,label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(required=True,label="Confirm Password", widget=forms.PasswordInput)
    
    def clean_username (self):
        username = self.cleaned_data["username"].lower()
        r = UserBase.objects.filter(username = username)
        if r.count():
           raise forms.ValidationError("Username already exists")
        return username
    
    def clean_password2 (self):
        data = self.cleaned_data 
        if data["password"] != data['password2']:
            raise forms.ValidationError("Passwords do not match")
        return data["password2"]
    
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Email', "id": "email"})
        self.fields['password'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Repeat Password'})
        
        
class EditForm (forms.ModelForm):
    class Meta:
        model = UserBase
        fields = ("email","last_name","first_name",) 
        
    email = forms.EmailField(
    label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    last_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-last_name',  }))

    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))
    
    def clean_email(self):
        form_email = self.cleaned_data['email'] 
        if self.instance and self.instance.email != form_email:
            raise forms.ValidationError("Email address cannot be changed.")
        return form_email
    
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['email'].required = True
    
    
    
    