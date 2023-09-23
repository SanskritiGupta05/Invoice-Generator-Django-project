from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class UserLogin(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        labels = {
            'username': 'UserId',
            'password': 'password'
        }

    def __init__(self, *args, **kwargs):
        super(UserLogin, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = ['company_name', 'gst_number', 'country', 'state', 'address']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        
        self.fields['company_name'].widget.attrs['class'] = 'form-control'
        self.fields['gst_number'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['gst_number'].widget.attrs['class'] = 'form-control'


class ServicesForm(forms.ModelForm):
    
    class Meta:
        model = Services
        fields = ['client', 'description', 'quantity', 'amount']
    
    def __init__(self, *args, **kwargs):
        super(ServicesForm, self).__init__(*args, **kwargs)
        self.fields['client'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['quantity'].widget.attrs['class'] = 'form-control'
        self.fields['amount'].widget.attrs['class'] = 'form-control'



class ServiceProviderForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['client', 'company_name', 'handle_by', 'email', 'phone',
                  'account_number', 'ifsc_code', 'bank_name', 'gst_number']

    def __init__(self, *args, **kwargs):
        super(ServiceProviderForm, self).__init__(*args, **kwargs)

        self.fields['client'].widget.attrs['class'] = 'form-control'
        self.fields['company_name'].widget.attrs['class'] = 'form-control'
        self.fields['handle_by'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['account_number'].widget.attrs['class'] = 'form-control'
        self.fields['ifsc_code'].widget.attrs['class'] = 'form-control'
        self.fields['bank_name'].widget.attrs['class'] = 'form-control'
        self.fields['gst_number'].widget.attrs['class'] = 'form-control'
