from django.urls import path


from .views import *


app_name = 'users'


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', CreateUser.as_view(), name='register'),
    path('profile/<slug:profile_slug>/',
         ProfileDetailView.as_view(), name='profile'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('change_pass/', ChangePassw.as_view(), name='change_pass'),
    path('change_pass/done/', ChangePasswDone.as_view(),
         name='change_pass_done'),
    path("change_username/", ChangeUsername.as_view(), name="change_username"),
    path('subscribe/<slug:profile_slug>/', subscribe_view, name='subscribe'),
    path("password_reset/", PasswordResetViewP.as_view(), name="password_reset"),
    path("password_reset_done/", PasswordResetDoneViewP.as_view(),
         name="password_reset_done"),
    path("password_reset/<uidb64>/<token>/",
         PasswordResetConfirmViewP.as_view(), name="password_reset_confirmm"),
    path("edit/", SettingsUser.as_view(), name="edit"),

]
