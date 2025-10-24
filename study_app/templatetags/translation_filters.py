from django import template
from django.utils.translation import gettext as _

register = template.Library()

@register.filter
def trans_title(title):
    """Translate book titles using Django's translation system"""
    return _(title)
