from django.contrib import admin
from app.models import Tag,Category,Comment,Post,Reply,ForbiddenWord

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(ForbiddenWord)

