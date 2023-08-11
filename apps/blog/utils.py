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
        return Post.published.filter(author__in=User.objects.filter(username__in=User.objects.get(
            username=request.user.username).user.get_following_users().values_list('user__username', flat=True)))
    elif request.GET.get('tag_slug') is not None:
        tag = get_object_or_404(Tag, slug=request.GET.get('tag_slug'))
        return Post.published.filter(tags__in=[tag])
    return Post.published.all()
