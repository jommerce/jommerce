from django.shortcuts import render
from django.views.generic import DetailView
from django.utils import timezone
from .models import Post


def index(request):
    return render(request, "blog/index.html")


class PostDetailView(DetailView):
    template_name = "blog/post.html"
    model = Post
    queryset = Post.objects.filter(publication_date__lte=timezone.now())
