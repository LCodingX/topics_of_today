from django.contrib import admin
from .models import Comment, Post, Topic, Alert, Opinions, Like, Field, PostImage

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(Alert)
admin.site.register(Opinions)
admin.site.register(Like)
admin.site.register(Field)
admin.site.register(PostImage)