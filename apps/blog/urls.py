from django.urls import path

from .views import *


app_name = 'blog'

urlpatterns = [
    path('home/', HomePage.as_view(), name='home'),
    path('fashion/', HomePage.as_view(), name='fashion'),
    path('travel/', HomePage.as_view(), name='travel'),
    path('<int:post_id>/<slug:post_slug>/',
         PostDetail.as_view(), name='post_detail'),
    path("add_post/", AddPostView.as_view(), name="add_post"),
    path("comment/<int:post_id>/<slug:post_slug>/",
         AddCommentView.as_view(), name="post_comments"),
    path('search/', SearchView.as_view(), name='search'),
]
