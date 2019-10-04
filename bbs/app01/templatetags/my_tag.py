from django import template
from app01 import models
from django.db.models.functions import TruncMonth
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('left_menu.html')
def left_menu(username):
    article_list = models.Article.objects.filter(blog__site_name=username)
    tag_list = models.Tag.objects.filter(blog__site_name=username). \
        annotate(c=Count('article')).values('name', 'c', 'id')
    category_list = models.Category.objects.filter(blog__site_name=username). \
        annotate(c=Count('article')).values('name', 'c', 'id')
    archive_list = article_list.annotate(c_time=TruncMonth('create_time')).values('c_time').annotate(
        c=Count('c_time')).values('c_time', 'c')

    return locals()
