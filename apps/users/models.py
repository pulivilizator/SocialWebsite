from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='пользователь', related_name='user', db_index=True)
    slug = models.SlugField(max_length=50, verbose_name='URL', unique=True)
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d', blank=True, verbose_name='Фото профиля', default='users/Profile.png')
    birthday = models.DateField(blank=True, null=True)
    following = models.ManyToManyField(
        'self', verbose_name='Подписчик', related_name='followings', symmetrical=False, blank=True)

    class Meta:
        ordering = ['user']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self) -> str:
        return self.user.username

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'profile_slug': self.slug})

    def get_following_users(self):
        return self.following.all()
