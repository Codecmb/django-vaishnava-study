# Read the file
with open('./study_app/models.py', 'r') as f:
    lines = f.readlines()

# Fix line 238 specifically (adjust index since lines start at 0)
if len(lines) > 237:
    # Line 238 is index 237 in zero-based indexing
    line_237 = lines[237]  # This should be the def __str__ line
    
    # Check if it has proper indentation (should start with 8 spaces for methods in class)
    if not line_237.startswith('        def __str__'):
        # Fix the indentation
        lines[237] = '        def __str__(self):\\n'
    
    # Also check the return line
    if len(lines) > 238:
        line_238 = lines[238]
        if not line_238.startswith('            return'):
            lines[238] = '            return f"Quiz Attempt - {self.book.title} - {self.module.name} - Score: {self.score}/{self.total_questions}"\\n'

# Write back
with open('./study_app/models.py', 'w') as f:
    f.writelines(lines)

print("✓ Fixed specific indentation on line 238")
