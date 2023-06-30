from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms import fields
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer
from django.core.validators import RegexValidator
from app.models import Customer

class CustomerRegistrationForm(UserCreationForm):
  username=forms.CharField(label='username',validators=[RegexValidator('^[A-Za-z][A-Za-z]{5,29}$',message="Username Should only contain aleast 6 characters ")],widget=forms.TextInput(attrs={'class':'form-control'}))
  email=forms.CharField(label='email',validators=[  RegexValidator(  '^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$',  message="Email should be valid")],widget=forms.EmailInput(attrs={'class':'form-control'}))
  password1=forms.CharField(label='Password',validators=[RegexValidator('^(\w+\d+|\d+\w+)+$',message="Password should be a combination of Alphabets and Numbers")],widget=forms.PasswordInput(attrs={'class':'form-control'}))
  password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
  

class Meta:
  Model = User
  fields = ('username','email','password1','password2')
  field_order = ('username', 'email','password1','password2')
  widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
  'email':forms.EmailInput(attrs={'class':'form-control'}),
  'password1':forms.PasswordInput(attrs={'class':'form-control'}),
  'password2':forms.PasswordInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username= UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password=forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
  old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True,'class':'form-control'}))
  new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
  new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
  email = forms.EmailField(label=_("Email"),max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
  new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
  new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

class CustomerProfileForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = ['name','locality','city','state','pincode']
    widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}),'city':forms.Select(attrs={'class':'form-control'}),'state':forms.Select(attrs={'class':'form-control'}),'pincode':forms.NumberInput(attrs={'class':'form-control'})}