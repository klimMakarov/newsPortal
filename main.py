import re


def censor(value):
    swears = ['редиск', 'редисок']
    return re.sub(
        fr'\b({'|'.join(swears)})\b',
        lambda match: match.group(1)[0] + '***',
        value,
        flags=re.IGNORECASE
    )


print(censor('Редиска, ты, редиска, купи редисок и запусти Редис'))
# print(censor('Редиска, ты, редиска, купи редисок и запусти Редис'))