from django import template
from familypost.models import Post
from django.shortcuts import get_object_or_404
import magic 
import os
from django.conf import settings

register = template.Library()

@register.simple_tag
def PostAttrib(postid, userid):
    #return Test.objects.filter(test_id=test.id, user_id=user.id)
    #if Post.objects.filter(id=postid).likes.filter(id=userid).exists():
    thisPost = get_object_or_404(Post, id=postid)

    postattrib = {}
    if thisPost.likes.filter(id=userid).exists():
        postattrib['liked'] = True
    else:
        postattrib['liked'] = False

    postattrib['totallikes'] = thisPost.totalLikes


    return postattrib


@register.filter
def filetype(filename):    
    mime = magic.Magic(mime=True)
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, filename)
    return mime.from_file(full_tmp_path).split('/')[0]

@register.filter
def filetype2(filename):    
    mime = magic.Magic(mime=True)
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, filename)
    return mime.from_file(full_tmp_path)