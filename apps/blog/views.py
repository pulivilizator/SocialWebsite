from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib import messages

from selfBlog import settings
from .models import *
from .forms import *
from .utils import *

from slugify import slugify
import redis

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB, )

class HomePage(DataMixin, ListView):
    model = Post
    template_name = 'blog/pages/home_page.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('subscribe') is not None and not self.request.user.is_authenticated:
            context['redirect_to_login'] = True
        else:
            up_context = self.get_user_context(
                title='Блог', path=self.request.path, form_s=SearchForm())
            context.update(up_context)
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return create_queryset_for_homepage(self.request)


class PostDetail(DataMixin, DetailView):
    model = Post
    template_name = 'blog/pages/single_post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post,
                                 id=self.kwargs['post_id'],
                                 slug=self.kwargs['post_slug'],
                                 )
        if post.status == 'DF' and post.author != self.request.user:
            raise Http404
        parent_comments = post.comments.filter(parent=None).select_related('author')
        total_views = r.incr(f'post:{post.id}:views')
        up_context = self.get_user_context(title=post.title,
                                           post=post,
                                           form=AddCommentForm(),
                                           form2=AddCommentForm(),
                                           parent_comments=parent_comments,
                                           total_views=total_views)
        context.update(up_context)
        return context


@method_decorator(login_required, name='dispatch')
class AddPostView(DataMixin, CreateView):
    model = Post
    form_class = AddPostForm
    template_name = 'blog/pages/add_post.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        up_context = self.get_user_context(title='Добавить пост')
        context.update(up_context)
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print(self.request.FILES)
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])
        form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AddCommentView(DataMixin, CreateView):
    model = Comment
    form_class = AddCommentForm

    def get_success_url(self) -> str:
        post_id = self.kwargs['post_id']
        post_slug = self.kwargs['post_slug']
        return reverse_lazy('blog:post_detail', kwargs={'post_id': post_id, 'post_slug': post_slug})

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        author = self.request.user
        post = Post.objects.get(
            id=self.kwargs['post_id'], slug=self.kwargs['post_slug'])
        if parent_id := self.request.POST.get('parent_comment_id'):
            form.instance.parent = Comment.objects.get(id=parent_id)
        form.instance.post = post
        form.instance.author = author
        form.save()
        return super().form_valid(form)


class SearchView(DataMixin, FormView):
    form_class = SearchForm
    template_name = 'blog/pages/search.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        search_vector = SearchVector('title', 'content')
        search_query = SearchQuery(query)
        result = Post.published.annotate(search=search_vector, rank=SearchRank(
            search_vector, search_query)).filter(search=search_query).order_by('-rank')
        up_context = self.get_user_context(
            title='Результаты поиска', posts=result)
        context.update(up_context)
        return context
