from django import template

register = template.Library()


@register.filter
def toInt(obj):
    return int(obj)