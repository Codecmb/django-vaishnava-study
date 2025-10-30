from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get dictionary item by key in templates"""
    return dictionary.get(key, '')
