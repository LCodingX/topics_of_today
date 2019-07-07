from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Comment, Alert

@receiver(post_save, sender=Comment)
def create_alert(sender, instance, created, **kwargs):
    if created:
        Alert.objects.create(receiver=instance.post.author.profile,
        content=
        f"you have received a comment from {instance.author.username} saying {instance.comment[:50]}",
        href=f"/Post/{instance.post.id}/")