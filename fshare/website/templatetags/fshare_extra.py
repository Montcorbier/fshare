from django import template
register = template.Library()

@register.filter(name='human_size')
def human_size(size):
    unit = ["", "K", "M", "G"]
    idx = 0
    while idx < len(unit) and size > (1024 ** (idx + 1)):
        idx += 1
    return str(size // (1024 ** idx)) + unit[idx]

@register.filter(name='in_mb')
def in_mb(size):
    return str(size // 1024**2);
