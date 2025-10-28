import re

# Read our current work
with open('./study_app/models_current_work.py', 'r') as f:
    content = f.read()

# Function to fix indentation for a specific class
def fix_class_indentation(content, class_name):
    # Find the class
    class_pattern = rf'(class {class_name}.*?(?=class|\\Z))'
    matches = re.findall(class_pattern, content, re.DOTALL)
    
    if not matches:
        return content
    
    class_content = matches[0]
    
    # Fix method indentation (8 spaces)
    class_content = re.sub(r'^    def (.*?):$', r'        def \\1:', class_content, flags=re.MULTILINE)
    
    # Fix method content (12 spaces)
    class_content = re.sub(r'^        def.*\\n    (.*)$', r'        def.*\\n            \\1', class_content, flags=re.MULTILINE)
    
    # Fix class variables (4 spaces)
    class_content = re.sub(r'^   (\\w+ = .*)$', r'    \\1', class_content, flags=re.MULTILINE)
    
    # Replace the fixed class in content
    content = content.replace(matches[0], class_content)
    return content

# Fix specific classes that are causing issues
content = fix_class_indentation(content, 'QuizAttempt')
content = fix_class_indentation(content, 'QuizQuestion')

# Replace tabs with spaces
content = content.replace('\\t', '    ')

# Write the fixed version
with open('./study_app/models.py', 'w') as f:
    f.write(content)

print("✓ Fixed indentation while preserving all our work")
