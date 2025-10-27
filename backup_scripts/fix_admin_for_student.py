#!/usr/bin/env python3
import re

# Read the current admin.py
with open('study_app/admin.py', 'r') as f:
    content = f.read()

# Update the fieldsets to show this is read-only and auto-populated
new_content = re.sub(
    r"fieldsets.*?\)\),",
    """fieldsets = (
        ('Basic Information', {
            'fields': ('book', 'module', 'chapter', 'verse_reference')
        }),
        ('Question Content', {
            'fields': ('question_text', 'multiple_choice_options')
        }),
        ('Auto-populated Answers', {
            'fields': ('correct_answers', 'prabhupada_commentary', 'additional_guidance'),
            'description': 'These fields are automatically populated when students answer questions'
        }),
    ),""",
    content,
    flags=re.DOTALL
)

# Also make the fields read-only
new_content = re.sub(
    r"readonly_fields = \\[.*?\\]",
    "readonly_fields = ['correct_answers', 'prabhupada_commentary', 'additional_guidance']",
    new_content
)

with open('study_app/admin.py', 'w') as f:
    f.write(new_content)

print("✅ Updated admin interface for student auto-population")
