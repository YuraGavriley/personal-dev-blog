from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("logout", views.logout_view, name="logout"),
    path("posts", views.AllPostView.as_view(), name="all-posts"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="single-post"),

]
