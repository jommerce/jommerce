from django.shortcuts import render
from django.views.generic import DetailView
from .models import Post


def index(request):
    return render(request, "blog/index.html")


class PostDetailView(DetailView):
    template_name = "blog/post.html"
    model = Post
