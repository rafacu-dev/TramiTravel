from django import template

register = template.Library()

@register.filter
def toMoney(objet) -> str:
    l = str(objet).split(".")
    start = l[0]
    if len(l) == 1: return f"{start}.00"
    end =  l[1]
    if len(end) == 1: end += "0"
    return f"{start}.{end}"

@register.filter
def concatenate(obj,valor):
    return str(obj)+str(valor)