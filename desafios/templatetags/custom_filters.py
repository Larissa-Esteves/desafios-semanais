# dentro de desafios/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Retorna o valor de uma chave de um dicionário no template.
    Se a chave não existir, retorna None.
    """
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return None
