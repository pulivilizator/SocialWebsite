from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))


class CreateUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите Имя'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))
    email = forms.EmailField(label='Пароль', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ChangePassFormP(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите старый пароль'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль'}))
    new_password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите новый пароль'}))


class ChangeUsername(forms.Form):
    username = forms.CharField(label='Новое имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите новое имя'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Имя уже занято')
        return username
