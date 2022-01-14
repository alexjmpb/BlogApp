from django import template
from blog.models import Comment
from django.utils import dateformat
from django.utils.timezone import *

register = template.Library()

@register.filter(name='comment_count')
def comment_count(post):
    return len(Comment.objects.all().filter(parent_post__id=post.id))


@register.filter(name='blog_datetime_format')
def blog_datime_format(datetime_object):
    return dateformat.format(datetime_object, 'l, M jS, Y, f A')