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
        context['comments'] = comments.order_by("-date")
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        current_user = request.user

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user_name = current_user.username
            comment.user_email = current_user.email
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("single-post", args=[slug]))

        return render(request, "main_app/post-detail.html", context={
            "post": post,
            "comments": post.comments.all().order_by("-date")
            })


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None:
            context["posts"] = []
        else:
            context["posts"] = Post.objects.filter(slug__in=stored_posts)

        return render(request, "main_app/read-later.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_slug = request.POST["post_slug"]

        if post_slug not in stored_posts:
            stored_posts.append(post_slug)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect(reverse("starting-page"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("starting-page"))
