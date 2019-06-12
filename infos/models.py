from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Comment(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(
        default=timezone.now)
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE)
    post = models.ForeignKey('Post',
        on_delete=models.CASCADE,
        related_name="comments")

class Post(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField()
    date_created = models.DateTimeField(
        default=timezone.now)
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE)
    topic = models.ForeignKey('Topic', 
    on_delete=models.CASCADE,
    related_name="posts")

class Topic(models.Model):
    image = models.ImageField(default="topic_pics/default.jpg", 
    upload_to="topic_pics")
    name = models.CharField(max_length=30)
    date_created = models.DateTimeField(
        default=timezone.now)
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE)
