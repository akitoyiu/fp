from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import DateTimeField
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.core.files.storage import default_storage
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid
from PIL import Image, ImageOps
from .validators import validate_file_type
import magic 
import os
from django.conf import settings
import subprocess
import shlex

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length = 75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.strip()
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


# custom user ID folder for images upload
def user_directory_path(instance, filename):
        return 'images/user_{0}/{1}'.format(instance.user.id, filename)

class PostMedia(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_owner')
    file = models.FileField(validators=[validate_file_type], upload_to=user_directory_path)

    class Meta:
        verbose_name_plural = 'PostMedias'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        mime = magic.Magic(mime=True)
        oldpath = self.file.name
        full_tmp_path = os.path.join(settings.MEDIA_ROOT, self.file.path)
        
        if mime.from_file(full_tmp_path).split('/')[0] == "image":            
            image = Image.open(self.file.path)
            image = ImageOps.exif_transpose(image)

            w, h = image.size
            resize = 640
            if w > resize or h > resize:    
                if w >= h:
                    h = int(h/w * resize)
                    w = resize
                else:
                    w = int(w/h * resize)
                    h = resize

                image = image.resize((w, h), Image.ANTIALIAS)
                image.save(self.file.path)
        else:
            param = ' -strict -2 -vf format=yuv420p -vf scale=-2:480 -c:v libx264 -c:a aac -b:a 128k -movflags +faststart -f mp4 '            

            subprocess.call('ffmpeg -i ' + self.file.path + param  + self.file.path + '.mp4 -y', shell=True)
            if os.path.exists(self.file.path + '.mp4'):
                default_storage.delete(self.file.path)
                self.file = oldpath + '.mp4'
                super().save()


class Post(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length = 255)
    #title_tag = models.CharField(max_length = 255, default="FamilyBlog Post")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length = 255)
    tags = models.ManyToManyField(Tag, related_name='tags')
    body = RichTextField(blank=True, null=True)
    #body = models.TextField()
    post_date = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    postmedias = models.ManyToManyField(PostMedia, null=True, blank=True, related_name='postmedias')

    def post_to_now(self):
        to_now = datetime.now(ZoneInfo(settings.TIME_ZONE)) - self.post_date
        to_s = to_now.total_seconds()
        if to_s < 3600:
            result = str(int(to_s / 60)) + "s"
        elif to_s < 86400:
            result = str(int(to_s / 3600)) + "h" 
        elif to_s < 31536000:
            result = str(int(to_s / 86400)) + "d"     
        else:
            result = str(int(to_s / 31536000)) + "y"
        return result

    def totalLikes(self):
        return self.likes.count()

    def tag_str(self):
        tags_all = self.tags.all()
        tags_list = []
        for t in tags_all:
            tags_list.append(t.title)
        return ', '.join(tags_list)

    def __str__(self):
        return self.title + str(self.author) ##Default return for the object

    def get_absolute_url(self):
        #return reverse('Article_Detail', args=str(self.id))
        return reverse('Home')


class Category(models.Model):
    name = models.CharField(max_length = 255)
    slug = models.SlugField(unique = True) #null = True, blank = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #return reverse('Article_Detail', args=str(self.id))
        return reverse('Home')


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    bio = models.TextField()
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    www_url = models.CharField(max_length = 255, null=True, blank=True)
    ig_url = models.CharField(max_length = 255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            image = Image.open(self.profile_image.path)
            image = ImageOps.exif_transpose(image)

            w, h = image.size
            resize = 300

            if w > resize or h > resize:    
                if w >= h:
                    h = int(h/w * resize)
                    w = resize
                else:
                    w = int(w/h * resize)
                    h = resize

                image = image.resize((w, h), Image.ANTIALIAS)
                image.save(self.profile_image.path)


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    post_date = models.DateTimeField(auto_now_add = True)
    likes = models.ManyToManyField(User, related_name='blog_comments')
    
    def totalLikes(self):
        return self.likes.count()

    def __str__(self):
        return self.post.title + str(self.commenter) ##Default return for the object

    def get_absolute_url(self):
        return reverse('Article_Detail', args=str(self.post.id))
        #return reverse('Home')

