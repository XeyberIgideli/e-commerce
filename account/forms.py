from django import forms

from account.models import UserBase

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserBase
        fields = ('email', 'username',)

    username = forms.CharField(required=True, label='Username', help_text='Username must be unique', min_length=4, max_length=50)
    email = forms.EmailField(required=True, max_length=100,help_text='Enter valid email', error_messages={'required': 'Enter valid email'})
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
    
    
    