from django import template
from blog.models import *
from django.db.models import Count, Q
from django.utils import timezone

from ..models import *

from taggit.models import Tag
from datetime import timedelta

register = template.Library()


@register.inclusion_tag('blog/includes/menu.html')
def show_menu(path):
    menu = [{'title': 'Главная страница', 'url_name': 'home'},
            {'title': 'Fashion', 'url_name': 'fashion'},
            {'title': 'Travel', 'url_name': 'travel'},
            {'title': 'About', 'url_name': 'asd'},
            {'title': 'Contacts', 'url_name': 'dsa'}
            ]
    return {'menu': menu, 'path': path}


@register.inclusion_tag('blog/includes/children_comment.html')
def show_children_comments(comment, form, post_id, post_slug):
    comments = comment.children.all()
    return {'comments': comments, 'form': form, 'post_id': post_id, 'post_slug': post_slug}


@register.simple_tag
def get_similar_posts(post: Post):
    posts = Post.objects.filter(~Q(id=post.id), tags__in=post.tags.all()).annotate(
        s=Count('tags'), c=Count('comments')).order_by('-s').order_by('-c').distinct()[:5]
    if len(posts) == 0:
        posts = get_pupolated_posts()
    return posts


@register.simple_tag
def get_pupolated_posts(limit=5):
    now = timezone.now()
    start = now - timedelta(days=7)
    end = now - timedelta(days=0)
    return Post.objects.filter(Q(created__gte=start) & Q(created__lte=end)).annotate(
        s=Count('comments')).order_by('-s')[:limit]
