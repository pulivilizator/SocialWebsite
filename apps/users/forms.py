from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from .models import Profile


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
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email уже используется')
        return data


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


class ChangeProfileForm(forms.ModelForm):
    birthday = forms.DateField(label='Дата рождения', widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите дату рождения', 'type': 'date'}), required=False)

    class Meta:
        model = Profile
        fields = ('photo', 'birthday')


class PasswordResetFormP(PasswordResetForm):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
                                "autocomplete": "email", 'placeholder': 'Укажите Ваш Email', 'class': 'form-control'}),
    )


class NewPasswordResetForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label=("Новый пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",
                                   'placeholder': 'Введите новый пароль', 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=("Повторите пароль"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", 'placeholder': 'Повторите пароль', 'class': 'form-control'}),
    )


class UserSettingsForm(forms.Form):
    photo = forms.ImageField(label='Выбрать новое фото',
                             widget=forms.FileInput())
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите имя'}), required=False)
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}), required=False)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите Email'}))
    birthday = forms.DateField(label='Дата рождения', widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите дату рождения', 'type': 'date'}), required=False)

    class Meta:
        fields = ("photo", "first_name",
                  "last_name", "email", "birthday")

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email уже используется')
        return data
