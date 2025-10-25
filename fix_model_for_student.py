#!/usr/bin/env python3
import re

# Read the current models.py
with open('study_app/models.py', 'r') as f:
    content = f.read()

# Update the correct_answers field description
new_content = re.sub(
    r'correct_answers = models\.TextField\([^)]*\)',
    'correct_answers = models.TextField(blank=True, null=True, help_text="Auto-populated: The correct answer will be stored here after students attempt the question")',
    content
)

with open('study_app/models.py', 'w') as f:
    f.write(new_content)

print("✅ Updated correct_answers field for student auto-population")
