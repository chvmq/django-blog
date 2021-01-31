from django import template
from blog.models import Category
from django.db.models import F, Count

register = template.Library()


@register.simple_tag()
def get_categories():
    """Получение категорий для шаблона"""
    return Category.objects.all()


@register.inclusion_tag('blog/list_categories.html')
def show_categories():
    """"""
    categories = Category.objects.all()
    # categories = Category.object.annotate(cnt=Count('news', filter=F('is_published'))).filter(cnt__gt=0)
    return {"categories": categories}
