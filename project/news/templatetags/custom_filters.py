import re
from django import template


register = template.Library()

@register.filter()
def censor(value):
    return re.sub(
        r'(редиска|редисок|редиски)',
        lambda match: match.group(1)[0] + ('*' * (len(match.group(1))- 1)),
        value,
        flags=re.IGNORECASE
    )
