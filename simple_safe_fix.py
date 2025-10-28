# Read the backup file with our work
with open('./study_app/models_current_work.py', 'r') as f:
    lines = f.readlines()

# Simple manual fixes for known issues
fixed_lines = []
for i, line in enumerate(lines):
    # Fix specific known problematic lines
    if 'def \\1:' in line:
        # Skip this broken line
        continue
    elif '        def __str__(self):' in line and '            return' in lines[i+1] if i+1 < len(lines) else False:
        # This is correct, keep it
        fixed_lines.append(line)
    elif '    def __str__(self):' in line:
        # Fix 4-space indentation to 8 spaces
        fixed_lines.append('        def __str__(self):\\n')
    elif 'def __str__(self):' in line and line.startswith('            '):
        # Fix 12-space indentation to 8 spaces
        fixed_lines.append('        def __str__(self):\\n')
    else:
        # Keep all other lines as is
        fixed_lines.append(line)

# Write the fixed version
with open('./study_app/models.py', 'w') as f:
    f.writelines(fixed_lines)

print("✓ Applied safe indentation fixes")
