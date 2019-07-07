from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from infos.models import Topic

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
    related_name="profile")
    image = models.ImageField(default="profile_pics/default.jpg", 
    upload_to="profile_pics")
    topic1 = models.ForeignKey(Topic, on_delete=None,
     default=1, related_name="topic1")
    topic2 = models.ForeignKey(Topic,on_delete=None,
     default=2,related_name="topic2")
    topic3 = models.ForeignKey(Topic,on_delete=None,
     default=3,related_name="topic3")

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 200 or img.width > 200:
            img.thumbnail((200, 200))
            img.save(self.image.path)
