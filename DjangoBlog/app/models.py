from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_slug ,validate_image_file_extension ,DecimalValidator


class Tag (models.Model):
    tag_name = models.CharField(max_length=50)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.tag_name

class Category (models.Model):
    cat_name = models.CharField(max_length=50) 
    subscribers = models.ManyToManyField(User,null=True,blank=True)  

    def __str__(self):
        return self.cat_name
    def show_subscribers(self):
        return " | ".join([s.username for s in self.subscribers.all()])

class ForbiddenWord(models.Model):
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    word = models.CharField(max_length=50)
    def __str__(self):
        return self.word
# ---------------------------------------
class Post(models.Model):
    title = models.CharField(max_length=100)
    post_content =models.TextField(max_length=300,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_image = models.ImageField(upload_to="posts/images/", height_field=None, width_field=None,validators =[validate_image_file_extension],null=True,blank=True)


    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,null=True,blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts',null=True,blank=True)
    unlikes = models.ManyToManyField(User, related_name='unliked_posts',null=True,blank=True)

    def __str__(self):
        return self.title
    def likes_number(self):
        return self.likes.count()
    def unlikes_number(self):
        return self.unlikes.count()


# class Like(models.Model):
#     author = models.ForeignKey(User,on_delete=models.CASCADE)
#     post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_likes")

#     def __str__(self):
#         return self.author.username + self.post.title

class Comment(models.Model):

    content    = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_comments")

    def __str__(self):
        return self.author.username + self.post.title

class Reply(models.Model):
    content    = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="comment_replies")

    def __str__(self):
        return self.author.username + self.content


        
