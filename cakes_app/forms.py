from django import forms
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    r'^(\+7|7|8)\d{10}$',
    message='Телефон в формате +7XXXXXXXXXX / 7XXXXXXXXXX / 8XXXXXXXXXX',
)

class PhoneLoginForm(forms.Form):
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': 'form-control cake__textinput mb-2',
            'placeholder': 'Телефон',
            'inputmode': 'tel',
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control cake__textinput mb-2',
            'placeholder': 'Пароль',
        })
    )


class ProfileForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control my-2 cake__textinput',
            'placeholder': 'Введите ваше имя',
        })
    )
    phone = forms.CharField(
        label='Телефон',
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control my-2 cake__textinput',
            'placeholder': '+7XXXXXXXXXX',
            'inputmode': 'tel',
        })
    )
    email = forms.EmailField(
        label='Почта',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control my-2 cake__textinput',
            'placeholder': 'you@example.com',
        })
    )
