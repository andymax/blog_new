from django import template
register = template.Library()
from ..models import Post,Category,Tags
from django.db.models.aggregates import Count
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
# @register.filter(name='transfer')
# def transfer(value, arg):
#     """将输出强制转换为字符串 arg """
#     return arg
#
# @register.filter()
# def lower(value):
#     """将字符串转换为小写字符"""
#     return value.lower()

from django.utils import timezone
import math

# 获取相对时间
@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
        return str(math.floor(diff.seconds / 60)) + "分钟前"

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
        return str(math.floor(diff.seconds / 3600)) + "小时前"

    if diff.days >= 1 and diff.days < 30:
        return str(diff.days) + "天前"

    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + "个月前"

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + "年前"



@register.inclusion_tag('article/inclusions/_recent_posts.html',takes_context=True)
def show_recent_posts(context,num=5):
    return {
        'recent_post_list':Post.objects.all().order_by('-views')[:num],
    }

@register.inclusion_tag('article/inclusions/_archives.html',takes_context=True)
def show_archives(context):
    return {

        'date_list': Post.objects.dates('create_time', 'month', order='DESC'),
    }


@register.inclusion_tag('article/inclusions/_categories.html',takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list
    }


@register.inclusion_tag('article/inclusions/_tags.html',takes_context=True)
def show_tags(context):
    tag_list = Tags.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tags_list':tag_list
    }

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return  Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()