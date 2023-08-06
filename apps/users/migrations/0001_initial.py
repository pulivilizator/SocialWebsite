# Generated by Django 4.2.3 on 2023-08-05 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('following', models.ManyToManyField(blank=True, related_name='followings', to='users.profile', verbose_name='Подписчик')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
                'ordering': ['user'],
            },
        ),
    ]