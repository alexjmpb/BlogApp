from django import template
from blog.models import Comment

register = template.Library()

@register.filter(name='comment_count')
def comment_count(post):
    return len(Comment.objects.all().filter(parent_post__id=post.id))