from django import forms
from django.core.exceptions import ValidationError
# models.
from .models import CastomUser


class RegisterUserForm(forms.Form):
    email = forms.EmailField(label='Почта', max_length=200)
    nickname = forms.CharField(label="Ваш ник", max_length=100)
    password = forms.CharField(label='Пароль', min_length=6)
    password2 = forms.CharField(label='Повторите пароль', min_length=6)
    
    def clean(self):
        return super().clean()
    
    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise ValidationError('Пароли не совпадают!')
        return self.cleaned_data


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = CastomUser
        fields = ('email', 'password')
