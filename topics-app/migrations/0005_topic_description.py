# Generated by Django 2.2 on 2019-06-12 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0004_topic_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='description',
            field=models.TextField(default='suck my coooooooooock'),
            preserve_default=False,
        ),
    ]
