from .models import Post

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth import logout


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.object)
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("single-post", args=[slug]))

        return render(request, "main_app/post-detail", context={
            "post": post,
            "comments": post.comment.all().order_by("-date")
            })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("starting-page"))
