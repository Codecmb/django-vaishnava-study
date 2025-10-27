from django import template

register = template.Library()

@register.filter
def get_field(form, question_id):
    """Get form field for a specific question"""
    field_name = f'question_{question_id}'
    return form[field_name]

@register.filter
def json_to_list(value):
    """Convert JSON string to Python list"""
    import json
    if value:
        try:
            return json.loads(value)
        except:
            return []
    return []
