from .models import Post

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Post


class StartingPageView(ListView):

    model = Post
    template_name = "main_app/index.html"
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostView(ListView):
    model = Post
    template_name = "main_app/all-posts.html"
    ordering = ["-date"]
    context_object_name = "all_posts"


class SinglePostView(DetailView):
    model = Post
    template_name = "main_app/post-detail.html"
    context_object_name = "post"

