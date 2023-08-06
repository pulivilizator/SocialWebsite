from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import User
from django.utils import timezone

from .models import *

from taggit.models import Tag
from datetime import timedelta


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        populate_tags = Tag.objects.annotate(
            s=Count('post')).order_by('-s')[:10]
        auth = self.request.user.is_authenticated
        if auth:
            context['profile_slug'] = self.request.user.username
        context['auth'] = auth
        context['p_tags'] = populate_tags
        return context


def create_queryset_for_homepage(request: WSGIRequest):
    if request.GET.get('subscribe') is not None:
        return Post.objects.filter(author__in=User.objects.filter(username__in=User.objects.get(
            username=request.user.username).user.get_following_users().values_list('user__username', flat=True)))
    elif request.GET.get('tag_slug') is not None:
        tag = get_object_or_404(Tag, slug=request.GET.get('tag_slug'))
        return Post.objects.filter(tags__in=[tag])
    return Post.objects.all()


def get_similar_posts(post: Post):
    posts = Post.objects.filter(~Q(id=post.id), tags__in=post.tags.all()).annotate(
        s=Count('tags'), c=Count('comments')).order_by('-s').order_by('-c').distinct()[:5]
    if len(posts) == 0:
        posts = get_pupolated_posts()
    return posts


def get_pupolated_posts(limit=5):
    now = timezone.now()
    start = now - timedelta(days=7)
    end = now - timedelta(days=0)
    return Post.objects.filter(Q(created__gte=start) & Q(created__lte=end)).annotate(
        s=Count('comments')).order_by('-s')[:limit]
