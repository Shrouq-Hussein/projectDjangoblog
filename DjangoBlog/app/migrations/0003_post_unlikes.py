# Generated by Django 4.1.3 on 2022-11-21 19:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_post_likes_alter_category_subscribers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='unlikes',
            field=models.ManyToManyField(blank=True, null=True, related_name='unliked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]