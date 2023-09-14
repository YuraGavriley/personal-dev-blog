from .models import Post, Comment, UserData

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views import View
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


class SinglePostView(View):
    # Check if post is saved for read later
    def is_saved_post(self, request, post_slug):
        if request.user.is_authenticated:
            username = request.user.username
            record = UserData.objects.get(username=username)
            stored_posts = record.stored_posts
        else:
            stored_posts = request.session.get("stored_posts")

        if stored_posts is not None:
            is_saved = post_slug in stored_posts
        else:
            is_saved = False

        return is_saved

    # Show content of posts during GET request
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = Comment.objects.filter(post=post)

        context = {}
        context["post"] = post
        context["comments"] = comments.order_by("-date")
        context["comment_form"] = CommentForm()
        context["is_saved_post"] = self.is_saved_post(request, post.slug)

        return render(request, "main_app/post-detail.html", context)

    # Implement comment handling by POST request
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

        return render(
            request,
            "main_app/post-detail.html",
            context={"post": post, "comments": post.comments.all().order_by("-date")},
        )


class ReadLaterView(View):
    # Function to add or delete slug from stored post list
    def add_or_delete_slug(self, post_slug, stored_posts):
        if post_slug not in stored_posts:
            stored_posts.append(post_slug)
        else:
            stored_posts.remove(post_slug)
        return stored_posts

    # Handling get request of the read later page
    def get(self, request):
        # Function to create context data for template
        def make_context(stored_posts):
            context = {}
            if stored_posts is None or len(stored_posts) == 0:
                context["posts"] = []
                context[
                    "has_posts"
                ] = False  # key, value pair for showing saved post status in html
            else:
                context["posts"] = Post.objects.filter(slug__in=stored_posts)
                context["has_posts"] = True
            return context

        stored_posts = request.session.get("stored_posts")

        # If user is authenticated, receive saved post data from database
        if request.user.is_authenticated:
            username = request.user.username
            try:
                record = UserData.objects.get(username=username)
            except UserData.DoesNotExist:
                if stored_posts is None:
                    stored_posts = []
                record = UserData(username=username, stored_posts=stored_posts)
                record.save()

            context = make_context(stored_posts=record.stored_posts)

        # Else receive data from sessions
        else:
            context = make_context(stored_posts=stored_posts)

        return render(request, "main_app/read-later.html", context)

    # Function for adding and deleting saved posts
    def post(self, request):
        stored_posts = request.session.get("stored_posts")
        post_slug = request.POST["post_slug"]
        if stored_posts is None:
            stored_posts = []

        # If user is authenticated, save/delete post to/from the database
        if request.user.is_authenticated:
            username = request.user.username
            try:
                record = UserData.objects.get(username=username)
                if record.stored_posts is None or len(record.stored_posts) == 0:
                    stored_posts = []
                stored_posts = self.add_or_delete_slug(post_slug, record.stored_posts)
                record.stored_posts = stored_posts
                record.save()
            except UserData.DoesNotExist:
                record = UserData(username=username, stored_posts=stored_posts)
                record.save()
        # Else, use session data to add or delete saved post
        else:
            stored_posts = self.add_or_delete_slug(post_slug, stored_posts)
            request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect(reverse("starting-page"))


class AboutView(TemplateView):
    template_name = "main_app/about.html"


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("starting-page"))


def pdf_view(request):
    with open(
        "main_app/static/main_app/files/CV - Yurii Stopchytskyi.pdf", "rb"
    ) as pdf:
        response = HttpResponse(pdf.read(), content_type="application/pdf")
        response["Content-Disposition"] = "inline;filename=mypdf.pdf"
        return response
