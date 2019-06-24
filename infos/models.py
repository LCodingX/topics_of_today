from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator
class Alert(models.Model):
    content = models.CharField(max_length=100)
    href = models.CharField(max_length=50)
    receiver = models.ForeignKey('users.Profile', 
    on_delete=models.CASCADE, related_name="alerts")

class Comment(models.Model):
    comment = models.TextField()
    date_created = models.DateTimeField(
        default=timezone.now)
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE)
    post = models.ForeignKey('Post',
        on_delete=models.CASCADE,
        related_name="comments")

class Like(models.Model):
    author = models.ForeignKey("users.Profile", 
    on_delete=models.CASCADE,related_name="likes")
    post = models.ForeignKey("infos.Post",
    on_delete=models.CASCADE, related_name="likes")

class Post(models.Model):
    title = models.CharField(max_length=60)
    content = models.TextField()
    views = models.IntegerField(default=0)
    date_created = models.DateTimeField(
        default=timezone.now)
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE,
        related_name="posts")
    topic = models.ForeignKey('Topic', 
    on_delete=models.CASCADE,
    related_name="posts")
    opinion = models.IntegerField(choices=(
        (-1, None),
        (0, 'Choice 1'),
        (1, 'Choice 2'),
        (2, 'Choice 3')
    ))

    def get_absolute_url(self):
        return reverse("infos-post", kwargs={"pk": self.pk})

class PostImage(models.Model):
    image = models.ImageField(
        upload_to='post_pics'
    )
    width_x = models.IntegerField(default=100,
        validators=[
            MaxValueValidator(500),
            MinValueValidator(100)
        ])
    width_y = models.IntegerField(default=1,
        validators=[
            MaxValueValidator(500),
            MinValueValidator(100)
        ])

    # Foreign Key to Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
    null=True, blank=True, related_name='images')
    def save(self, *args, **kwargs):
        super(PostImage, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > self.width_y or img.width > self.width_x:
            img.thumbnail((self.width_x, self.width_y))
            img.save(self.image.path)

class Opinions(models.Model):
    desc1 = models.CharField(max_length=100, blank=True)
    desc2 = models.CharField(max_length=100, blank=True)
    desc3 = models.CharField(max_length=100,blank=True)
    topic = models.OneToOneField("infos.Topic",
    on_delete=models.CASCADE, related_name="opinions")

class Field(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Topic(models.Model):
    field = models.ForeignKey(Field, 
    on_delete=models.CASCADE, related_name="topics")
    views = models.IntegerField(default=0)
    image = models.ImageField(default=
    "topic_pics/default.jpg", 
    upload_to="topic_pics")
    description = models.CharField(max_length=200)
    name = models.CharField(max_length=30)
    date_created = models.DateTimeField(
        default=timezone.now)
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Topic, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 200 or img.width > 200:
            img.thumbnail((200, 200))
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("infos-topic", kwargs={"pk": self.pk})
