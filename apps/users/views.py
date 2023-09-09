from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.views.generic import CreateView, FormView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *
from .forms import *
from blog.utils import DataMixin
from mailings.models import Mailing


class LoginUser(DataMixin, views.LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('blog:home')
    form_class = LoginForm

    def get_success_url(self) -> str:
        return reverse_lazy('blog:home')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        if self.request.user.is_authenticated:
            return redirect('users:profile')
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Вход')
        context.update(up_context)
        return context


@method_decorator(login_required, name='dispatch')
class LogoutUser(DataMixin, views.LogoutView):
    success_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy('users:login')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Выход')
        context.update(up_context)
        return context


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DataMixin, DetailView):
    model = Profile
    template_name = "users/profile.html"
    slug_url_kwarg = 'profile_slug'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, slug=self.kwargs['profile_slug'])
        my_profile = self.request.user.username == self.kwargs['profile_slug']
        user_profile = Profile.objects.get(user=self.request.user)
        following = bool(my_profile or profile.followings.filter(
            slug=user_profile.slug))
        up_context = self.get_user_context(
            title='Профиль', profile=profile, my_profile=my_profile, following=following)
        context.update(up_context)
        return context


class CreateUser(DataMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('blog:home')

    def get_success_url(self) -> str:
        return reverse_lazy('blog:home')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Регистрация')
        context.update(up_context)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save()
        login(self.request, user)
        u = User.objects.get(username=form.cleaned_data['username'])
        profile = Profile(user=u, slug=u.username)
        profile.save()
        mailing = Mailing(user=u, active=True)
        mailing.save()
        return redirect('blog:home')


@method_decorator(login_required, name='dispatch')
class ChangePassw(DataMixin, views.PasswordChangeView):
    form_class = ChangePassFormP
    template_name = 'users/change_pass.html'
    success_url = reverse_lazy('users:change_pass_done')

    def get_success_url(self) -> str:
        return reverse_lazy('users:change_pass_done')

    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Смена пароля')
        context.update(up_context)
        return context

    def form_valid(self, form):
        old_password = form.cleaned_data.get('old_password')
        new_password1 = form.cleaned_data.get('new_password1')

        if new_password1 == old_password:
            form.add_error('new_password1',
                           'Новый пароль должен отличаться от предыдущего.')
            return self.form_invalid(form)

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ChangePasswDone(DataMixin, views.PasswordChangeDoneView):
    template_name = 'users/change_pass_done.html'
    success_url = reverse_lazy('users:profile')

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile')

    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Успешная смена пароля')
        context.update(up_context)
        return context


@method_decorator(login_required, name='dispatch')
class ChangeUsername(DataMixin, FormView):
    form_class = ChangeUsername
    template_name = 'users/change_username.html'
    success_url = reverse_lazy('users:profile')

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', kwargs={'profile_slug': self.kwargs['profile_slug']})

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Смена имени пользователя')
        context.update(up_context)
        return context

    def form_valid(self, form: Any) -> HttpResponse:
        user = User.objects.get(username=self.request.user.username)
        new_username = form.cleaned_data['username']
        user.username = new_username
        profile = Profile.objects.get(user=user)
        profile.slug = new_username
        user.save()
        profile.save()
        self.kwargs['profile_slug'] = new_username
        return super().form_valid(form)


@login_required
def subscribe_view(request: WSGIRequest, profile_slug):
    subscriber = Profile.objects.get(slug=request.user.username)
    bloger = Profile.objects.get(slug=profile_slug)
    if not int(request.GET.get('following')):
        subscriber.following.add(bloger)
    else:
        subscriber.following.remove(bloger)
    return redirect('users:profile', profile_slug=profile_slug)


class PasswordResetViewP(DataMixin, views.PasswordResetView):
    form_class = PasswordResetFormP
    template_name = 'users/password_reset/password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/password_reset/password_reset_message.html'

    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Сброс пароля')
        context.update(up_context)
        return context


class PasswordResetDoneViewP(DataMixin, views.PasswordResetDoneView):
    success_url = reverse_lazy('users:login')
    template_name = 'users/password_reset/password_reset_done.html'

    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Письмо отправлено')
        context.update(up_context)
        return context


class PasswordResetConfirmViewP(DataMixin, views.PasswordResetConfirmView):
    template_name = 'users/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')
    form_class = NewPasswordResetForm

    def get_context_data(self, **kwargs: Any) -> Any:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Письмо отправлено')
        context.update(up_context)
        return context


@method_decorator(login_required, name='dispatch')
class SettingsUser(DataMixin, FormView):
    form_class = UserSettingsForm
    template_name = 'users/user_settings.html'
    success_url = reverse_lazy('users:profile')

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', kwargs={'profile_slug': self.kwargs['profile_slug']})

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(
            title='Настройка профиля', user=self.request.user)
        context.update(up_context)
        return context

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        user = self.request.user
        self.kwargs['profile_slug'] = user.username
        initial['photo'] = user.user.photo
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        initial['birthday'] = user.user.birthday
        return initial

    def form_valid(self, form: Any) -> HttpResponse:
        user = User.objects.get(username=self.request.user.username)
        profile = user.user

        if first_name := form.cleaned_data['first_name']:
            user.first_name = first_name

        if last_name := form.cleaned_data['last_name']:
            user.last_name = last_name

        if email := form.cleaned_data['email']:
            user.email = email

        if photo := form.cleaned_data['photo']:
            profile.photo = photo

        if birthday := form.cleaned_data['birthday']:
            profile.birthday = birthday

        user.save()
        profile.save()

        return super().form_valid(form)


@login_required
def sub_update_site(request: WSGIRequest):
    user_mailing = request.user.mailing
    if not user_mailing.active:
        user_mailing.active = True
        user_mailing.save()
    return redirect('users:profile', profile_slug=request.user.username)


@login_required
def unsub_update_site(request: WSGIRequest):
    user_mailing = request.user.mailing
    if user_mailing.active:
        user_mailing.active = False
        user_mailing.save()
    return redirect('users:profile', profile_slug=request.user.username)
