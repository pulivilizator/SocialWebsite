# Generated by Django 4.2.3 on 2023-08-05 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Основной текст')),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name='Фото')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время публикации')),
                ('slug', models.SlugField(max_length=255)),
                ('status', models.CharField(choices=[('DF', 'Черновик'), ('PB', 'Опубликовать')], default='DF', max_length=10, verbose_name='Статус')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
                'ordering': ['-publish'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Контент')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='Активен')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='users.profile', verbose_name='Автор')),
                ('parent', mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blog.comment', verbose_name='Родительский комментарий')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
                'ordering': ['-created'],
            },
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-publish'], name='blog_post_publish_bb7600_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['-created', 'post', 'author', 'parent'], name='blog_commen_created_43ad85_idx'),
        ),
    ]