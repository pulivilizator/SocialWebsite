from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.views.generic import ListView, DetailView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import *
from .forms import *
from .utils import *

from slugify import slugify


class HomePage(DataMixin, ListView):
    model = Post
    template_name = 'blog/pages/home_page.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('subscribe') is not None and not self.request.user.is_authenticated:
            context['redirect_to_login'] = True
        else:
            self.queryset = create_queryset_for_homepage(self.request)
            up_context = self.get_user_context(
                title='Блог', path=self.request.path)
            context.update(up_context)
        return context


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
                                 status=Post.Status.PUBLISH)
        # similar_posts = get_similar_posts(post)
        parent_comments = post.comments.filter(parent=None)
        up_context = self.get_user_context(
            title=post.title, post=post, form=AddCommentForm(), form2=AddCommentForm(), parent_comments=parent_comments)
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
