from django import template

register = template.Library()


@register.filter
def replace_underscores(value):
    """
    Заменяет нижние подчеркивания на пробелы.
    """
    if isinstance(value, str):
        return value.replace('_', ' ')