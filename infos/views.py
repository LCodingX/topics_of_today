from django.shortcuts import render
from .models import Post, Topic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'home'
    }
    return render(request, "infos/home.html", context)
@login_required
def topics(request):
    context = {
        'topics': Topic.objects.all(),
        'title': 'topics'
    }
    return render(request, "infos/topics.html", context)
@login_required
def trending(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'trending'
    }
    print(Post.objects.first().comments)
    return render(request, "infos/trending.html", context)
class post(DetailView):
    model = Post
    template_name = "infos/post.html"
    context_object_name = "post"
