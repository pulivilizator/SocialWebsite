from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey

from users.models import Profile


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)


class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.DRAFT)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISH = 'PB', 'Опубликовать'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Основной текст')
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d', blank=True, verbose_name='Фото')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    publish = models.DateTimeField(
        default=timezone.now, verbose_name='Время публикации')
    slug = models.SlugField(max_length=255)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')

    objects = models.Manager()
    published = PublishManager()
    draft = DraftManager()

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.pk, "post_slug": self.slug})


class Comment(MPTTModel):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments')
    content = models.TextField(verbose_name='Контент', max_length=150)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name='Активен')
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий',
                            null=True, related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        order_insertion_by = ('-created')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(
            fields=['-created', 'post', 'author', 'parent'])]
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self) -> str:
        return f'{self.author}: {self.content}'
