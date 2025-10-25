#!/usr/bin/env python3
import re

# Read the current urls.py
with open('study_app/urls.py', 'r') as f:
    content = f.read()

# Remove the problematic line we just added
new_content = re.sub(
    r"# Add professional quiz URL pattern.*?take_quiz_professional\),",
    "",
    content,
    flags=re.DOTALL
)

# Write it back
with open('study_app/urls.py', 'w') as f:
    f.write(new_content)

print("✅ Removed problematic URL line")
