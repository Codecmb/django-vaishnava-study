import os

# Read the current settings
with open('website/settings.py', 'r') as f:
    content = f.read()

# Update the TEMPLATES DIRS to include the templates directory
old_templates = """'DIRS': [],"""
new_templates = """'DIRS': [os.path.join(BASE_DIR, 'templates')],"""

if old_templates in content:
    content = content.replace(old_templates, new_templates)
    with open('website/settings.py', 'w') as f:
        f.write(content)
    print("✓ Updated TEMPLATES DIRS in settings.py")
else:
    print("✗ Could not find TEMPLATES DIRS to update")
