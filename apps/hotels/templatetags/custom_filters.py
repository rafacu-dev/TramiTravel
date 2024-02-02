from django import template
from datetime import datetime

register = template.Library()


@register.filter
def toInt(obj):
    return int(obj)

@register.filter
def parseFloat(obj):
    return str(obj).replace(",",".")


@register.filter
def toMoney(objet) -> str:
    l = str(objet).split(".")
    start = l[0]
    if len(l) == 1: return f"{start}.00"
    end =  l[1]
    if len(end) == 1: end += "0"
    return f"{start}.{end}"


@register.filter
def toDate(obj):
    return datetime.strptime(obj, "%m/%d/%Y")


@register.filter
def parseUrl(obj):
    return obj.replace("/","%2F")