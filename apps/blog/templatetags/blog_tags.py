from django import template
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.safestring import mark_safe

from ..models import *
from blog.models import *

from taggit.models import Tag
from datetime import timedelta
import markdown

register = template.Library()


@register.inclusion_tag('blog/includes/menu.html')
def show_menu(path):
    menu = [{'title': 'Главная страница', 'url_name': 'home'},
            ]
    return {'menu': menu, 'path': path}


@register.inclusion_tag('blog/includes/children_comment.html')
def show_children_comments(comment, form, post_id, post_slug):
    comments = comment.children.all()
    return {'comments': comments, 'form': form, 'post_id': post_id, 'post_slug': post_slug}


@register.simple_tag
def get_similar_posts(post: Post):
    posts = Post.objects.filter(~Q(id=post.id), tags__in=post.tags.all(), status=Post.Status.PUBLISH).annotate(
        s=Count('tags'), c=Count('comments')).order_by('-s').order_by('-c').distinct()[:5]
    if len(posts) == 0:
        posts = get_pupolated_posts()
    return posts


@register.simple_tag
def get_pupolated_posts(limit=5):
    now = timezone.now()
    start = now - timedelta(days=7)
    end = now - timedelta(days=0)
    return Post.objects.filter(Q(created__gte=start) & Q(created__lte=end), status=Post.Status.PUBLISH).annotate(
        s=Count('comments')).order_by('-s')[:limit]


@register.filter(name='markdown')
def makdown_format(text):
    return mark_safe(markdown.markdown(text))
