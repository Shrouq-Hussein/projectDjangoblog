# Generated by Django 4.1.3 on 2022-11-21 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='app.post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='app.tag'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_replies', to='app.comment'),
        ),
    ]
