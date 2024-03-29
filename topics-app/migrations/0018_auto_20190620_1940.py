# Generated by Django 2.2 on 2019-06-21 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0017_auto_20190617_2014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='field',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='infos.Field'),
            preserve_default=False,
        ),
    ]
