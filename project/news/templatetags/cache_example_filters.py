from django import template


register = template.Library()

@register.filter
def pow(value, pow):
    return value**pow

@register.filter
def short(value):
    str_value = str(value)
    if len(str_value) > 50:
        return f'{str_value[:50]}...'