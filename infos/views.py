from django.shortcuts import render, redirect
from .models import (
    Post, Topic, Comment, Alert, 
    Opinions, Like, Field, PostImage
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView, ListView, UpdateView
from datetime import timedelta
from django.utils import timezone
from django.db.models import F, Q
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.core.paginator import Paginator

def home(request):
    context = {
        'posts': Post.objects.all(),
        'title': 'Topics of Today',
    }
    if request.user.is_authenticated:
        context["topic1"]=request.user.profile.topic1
        context["topic2"]=request.user.profile.topic2
        context["topic3"]=request.user.profile.topic3
    return render(request, "infos/home.html", context)
@login_required
def topics(request):
    topics = Topic.objects.order_by("-views").filter(date_created__range = 
    [str(timezone.now().date() - timedelta(days=8)), str(timezone.now())])
    paginator = Paginator(topics, 10)
    page = request.GET["page"]
    topics = paginator.get_page(page)
    context = {
        "topics": topics,
        "title": "Topics of Today - Topics",
        'topic1': request.user.profile.topic1,
        'topic2': request.user.profile.topic2,
        'topic3': request.user.profile.topic3
    }
    return render(request, "infos/topics.html", context)
@login_required
def trending(request):
    posts = Post.objects.order_by("-views").filter(date_created__range = 
    [str(timezone.now().date() - timedelta(days=3)), str(timezone.now())])
    paginator = Paginator(posts, 10)
    page = request.GET["page"]
    posts = paginator.get_page(page)
    context = {
        "posts": posts,
        "title": "Topics of Today - Trending",
        'topic1': request.user.profile.topic1,
        'topic2': request.user.profile.topic2,
        'topic3': request.user.profile.topic3
    }
    return render(request, "infos/trending.html", context)
@login_required
def fields(request):
    fields = [
        Field.objects.get(name="Politics"),
        Field.objects.get(name="Memes"),
        Field.objects.get(name="Science/Tech"),
        Field.objects.get(name="Pop Culture"),
        Field.objects.get(name="Sports"),
        Field.objects.get(name="Movies/TV"),
    ]
    context = {
        'title' : "Topics Of Today - Fields",
        'fields': fields
    }
    return render(request, "infos/fields.html", context)
@login_required
def field(request, pk):
    field = Field.objects.get(pk=pk)
    topics = field.topics.all().order_by("-views")
    paginator = Paginator(topics, 10)
    page = request.GET["page"]
    topics = paginator.get_page(page)
    context = {
        'title': f'Topics of Today - Field {field.name}',
        'topics': topics
    }
    return render(request, "infos/field.html", context)
class CommentForm(forms.ModelForm):
    comment = forms.TextInput()
    class Meta:
        model = Comment
        fields=["comment"]
def redirecttotopic(request, pk):
    return redirect(f"/Topic/{pk}/?page=1")
class topic(LoginRequiredMixin, DetailView):
    model = Topic
    template_name = "infos/topic.html"
    context_object_name = "topic"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context["topic"].posts.all().order_by("-likes"),10)
        page = self.request.GET["page"]
        context["posts"] = paginator.get_page(page)
        context["title"] = f"{context['topic'].name} - Topics of Today"
        context['topic1'] = self.request.user.profile.topic1
        context['topic2'] = self.request.user.profile.topic2
        context['topic3'] = self.request.user.profile.topic3
        return context

    def dispatch(self, request, **kwargs):
        profile = request.user.profile
        topic_id = self.kwargs["pk"]
        if topic_id == profile.topic3.id:
            profile.topic2, profile.topic3 = profile.topic3, profile.topic2
        elif topic_id == profile.topic2.id:
            profile.topic1, profile.topic2 = profile.topic2, profile.topic1
        elif topic_id != profile.topic1.id:
            profile.topic3 = Topic.objects.get(pk=topic_id)
        profile.save()
        topic = Topic.objects.filter(pk=self.kwargs["pk"]).first()
        Topic.objects.filter(pk=self.kwargs["pk"]).update(views=F('views') + 1)
        views = topic.views
        if views in [50,100,1000,10000]:
            Alert.objects.create(content=
            f"Your topic {topic.name} has received {views} views",
            href=f"/Topic/{topic_id}/?page=1", receiver=topic.author.profile)

        return super().dispatch(request, **kwargs)

class post(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "infos/post.html"
    context_object_name = "post"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{context['post'].title} - Topics of Today"
        context['topic1'] = self.request.user.profile.topic1
        context['topic2'] = self.request.user.profile.topic2
        context['topic3'] = self.request.user.profile.topic3
        context["commentform"] = CommentForm()
        return context
    def dispatch(self, request, **kwargs):
        Post.objects.filter(pk=self.kwargs["pk"]).update(views=F('views') + 1)
        post = Post.objects.filter(pk=self.kwargs["pk"]).first()
        likes = post.likes.count()
        if likes in [10,50,100,1000]:
            Alert.objects.create(content=
            f"Your post {post.title} has received {likes} likes",
            href=f"/Post/{post.id}/", receiver=post.author.profile)
        views = post.views
        if views in [50,100,1000,10000]:
            Alert.objects.create(content=
            f"Your post {post.title} has received {views} views",
            href=f"/Post/{post.id}/", receiver=post.author.profile)
        return super().dispatch(request, **kwargs)

class TopicForm1(forms.ModelForm):
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=200)
    image = forms.ImageField(required=False)
    field = forms.ModelChoiceField(queryset=Field.objects.all())
    class Meta:
        model = Topic
        fields = ["name", "description", "image", "field"]
class TopicForm2(forms.ModelForm):
    desc1 = forms.CharField(max_length=100, required=False)
    desc2 = forms.CharField(max_length=100, required=False)
    desc3 = forms.CharField(max_length=100, required=False)
    class Meta:
        model=Opinions
        fields=["desc1", "desc2", "desc3"]
@login_required
def create_topic(request):
    if request.method == "GET":
        context = {
            'title': "Creating Topic on Topics of Today",
            'infoform':TopicForm1(prefix="infoform"),
            'opinionform':TopicForm2(prefix="opinionform"),
        }
        return render(request, "infos/create_topic.html", context)
    else:
        infoform = TopicForm1(request.POST, request.FILES, prefix="infoform")
        opinionform = TopicForm2(request.POST, prefix="opinionform")
        if infoform.is_valid() and opinionform.is_valid():
            withauthor1 = infoform.save(commit=False)
            withauthor1.author = request.user
            withauthor1.save()
            withauthor = opinionform.save(commit=False)
            withauthor.topic_id = withauthor1.id
            withauthor.save()
        else:
            print("data invalid")
        return redirect("/Topics/create/")

class PostImageForm(forms.ModelForm):
    image = forms.FileField()
    width_x = forms.IntegerField(max_value=500)
    width_y = forms.IntegerField(max_value=500)
    class Meta:
       model = PostImage
       fields = ["image", "width_x", "width_y"]

def uploadpostimg(request, pk):
    posts = Post.objects.filter(pk=pk)
    if posts.count == 0:
        return redirect("/")
    if posts.first().author != request.user:
        return redirect("/")
    if request.method == "GET":
        form = PostImageForm()
    else:
        form = PostImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.post = Post.objects.get(pk=pk)
            form.save()
            return redirect(f"/Post/{pk}")
    context = {
        'title': "Uploading Post Picture in Topics of Today",
        "form": form,
    }
    return render(request, "infos/upload_img.html", context)
class create_post(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "opinion"]
    template_name = "infos/create_post.html"
    def get_context_data(self, **kwargs):           
        context = super().get_context_data(**kwargs)
        context["title"] = f"Creating Post in Topic {self.topic} - Topics of Today"
        return context
    def dispatch(self, request, *args, **kwargs):
        self.topic = request.GET.get('topic', False)
        return super(create_post, self).dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic_id = self.topic
        form.save()
        return redirect(f"/upload/postimg/{form.instance.id}")

@login_required
def searchposts(request):
    if request.method == "POST":
        search = request.POST["search"]
        results = Post.objects.all().filter(Q(title__icontains=search) | 
        Q(content__icontains=search))
        context = {
        'title': "Searching Posts - Topics of Today",
        "postresults": results
         }
        return render(request, "infos/search.html", context)
    return redirect("/")
@login_required
def searchtopics(request):
    if request.method == "POST":
        search = request.POST["search"]
        results = Topic.objects.all().filter(Q(name__icontains=search))
    else:
        return redirect('/')
    context = {
        'title': f"Searching Topics - Topics of Today",
        "topicresults": results
    }
    return render(request, "infos/search.html", context)
@login_required
def searchall(request):
    if request.method == "POST":
        search = request.POST["search"]
        topicresults = Topic.objects.all().filter( Q(name__icontains=search) | Q(description__icontains=search) )
        postresults = Post.objects.all().filter( Q(title__icontains=search) | Q(content__icontains=search) )
    else:
        return redirect('/')
    context = {
        'title': "Searching Topics of Today",
        "postresults": postresults,
        "topicresults": topicresults
    }
    return render(request, "infos/search.html", context)
@login_required
def searchin(request, **kwargs):
    pk = kwargs["pk"]
    if request.method == "POST":
        topic = Topic.objects.get(pk=pk)
        if request.method == "POST":
            search = request.POST["search"]
            results = topic.posts.filter(Q(title__icontains=search) | 
            Q(content__icontains=search))
    else:
        return redirect("/")
    context = {
        "title": f"Searching in topic {pk} - Topics of Today",
        "postresults": results
    }
        
    return render(request, "infos/search.html", context)
@login_required
def searchuser(request, **kwargs):
    if request.method == "POST":
        pk = kwargs["pk"]
        user = User.objects.get(pk=pk)
        if request.method == "POST":
            search = request.POST["search"]
            results = user.posts.filter( Q(title__icontains=search) |
            Q(content__icontains=search) )
        context = {
            "postresults": results
        }
        return render(request, "infos/search.html", context)
    else:
        return redirect("/")
@login_required
def comment(request, pk):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        newcomment = Comment(comment = request.POST["comment"],
        post_id=pk, post=post, author=request.user)
        newcomment.save()
        return redirect(f"/Post/{pk}/")
@login_required
def deletepost(request, pk):
    if request.method == "POST":
        Post.objects.get(pk=pk).delete()
        return redirect("/")
    return redirect("/")
class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["opinion", "content", "title"]
    template_name="infos/update_post.html"

@login_required
def like(request, pk):
    user = request.user.profile
    if Post.objects.filter(pk=pk):
        post = Post.objects.get(pk=pk)
        if not Like.objects.filter(author=user,post=post):
            Like.objects.create(author=user, post=post)
        return redirect(f"/Post/{post.id}/")
    return redirect("/")

@login_required
def unlike(request, pk):
    user = request.user.profile
    if Post.objects.filter(pk=pk):
        post = Post.objects.get(pk=pk)
        if Like.objects.filter(author=user, post=post):
            Like.objects.get(author=user, post=post).delete()
        return redirect(f"/Post/{post.id}/")
    return redirect("/")