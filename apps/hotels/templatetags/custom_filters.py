from django import template

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