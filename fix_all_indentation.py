# Read the file
with open('./study_app/models.py', 'r') as f:
    lines = f.readlines()

# Fix indentation for all methods
fixed_lines = []
for i, line in enumerate(lines):
    # Fix method definitions (should have 8 spaces)
    if 'def ' in line and '(self):' in line and not line.startswith('        def '):
        if line.startswith('    def '):  # 4 spaces - needs 8
            line = '        ' + line[4:]
        elif line.startswith('            def '):  # 12 spaces - needs 8
            line = '        ' + line[12:]
        elif line.startswith('                def '):  # 16 spaces - needs 8
            line = '        ' + line[16:]
    
    # Fix return statements in methods (should have 12 spaces)
    elif 'return ' in line and 'def ' in lines[i-1] if i > 0 else False:
        if not line.startswith('            return '):
            if line.startswith('        return '):  # 8 spaces - needs 12
                line = '            ' + line[8:]
            elif line.startswith('                return '):  # 16 spaces - needs 12
                line = '            ' + line[16:]
            elif line.startswith('    return '):  # 4 spaces - needs 12
                line = '            ' + line[4:]
    
    fixed_lines.append(line)

# Write back
with open('./study_app/models.py', 'w') as f:
    f.writelines(fixed_lines)

print("✓ Fixed all indentation issues")
