# Read the file
with open('./study_app/models.py', 'r') as f:
    content = f.read()

# Fix all __str__ methods that have \n characters
import re

# Pattern to find broken __str__ methods
pattern = r'def __str__\(self\):\\n\s+return (.*?)\\n'

# Replace with proper method syntax
def fix_str_method(match):
    return_line = match.group(1)
    return f'def __str__(self):\\n        return {return_line}'

content = re.sub(pattern, fix_str_method, content)

# Write the fixed version
with open('./study_app/models.py', 'w') as f:
    f.write(content)

print("✓ Fixed all __str__ methods with backslash issues")
