from django import template

register = template.Library()

@register.filter
def get_field(form, question_id):
    """Get form field for a specific question"""
    field_name = f'question_{question_id}'
    return form[field_name]
