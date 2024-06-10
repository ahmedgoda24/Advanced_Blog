from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Profile

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
 
# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput
#     )
#     password2 = forms.CharField(
#         label='Repeat password',
#         widget=forms.PasswordInput
#     )

#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'first_name', 'email']

#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError("Passwords don't match.")
#         return cd['password2']

#     def clean_email(self):
#         data = self.cleaned_data['email']
#         if User.objects.filter(email=data).exists():
#             raise forms.ValidationError('Email already in use.')
#         return data

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username' , 'email','first_name','last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number' , 'addres']