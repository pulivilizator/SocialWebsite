from django import template
from blog.models import *


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
