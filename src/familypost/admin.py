from django.contrib import admin
from .models import Post, Category, UserProfile, PostComment, Tag, PostMedia
# Register your models here.
admin.site.register(Post) ## put this on the admin page
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(PostComment)
admin.site.register(Tag)
admin.site.register(PostMedia)