
"""| AUTHS FORMS |"""

# Django.
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
# models.
from .models import CastomUser, PageRequests


class RegisterUserForm(forms.Form):
    """ 
    REGISTRATION FORM 

    Параметры:
        - email (str)
        - name (str)
        - password (str)
        - password2 (str)
    """
    email = forms.EmailField(label='Почта', max_length=200)
    name = forms.CharField(label="Имя", max_length=100)
    password = forms.CharField(label='Пароль', min_length=6)
    password2 = forms.CharField(label='Повторите пароль', min_length=6)
    
    def clean(self):
        return super().clean()
    
    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise ValidationError('Пароли не совпадают!')
        return self.cleaned_data


class LoginUserForm(forms.Form):
    """
    LOGIN FORM

    Параметры:
        - email (str)
        - password (str)
    """
    email = forms.EmailField(label='Почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError('Неверные учетные данные')

        return cleaned_data
