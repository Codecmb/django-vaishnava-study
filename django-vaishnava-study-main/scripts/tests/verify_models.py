#!/bin/bash
echo "🔍 VERIFYING MODELS.PY"
echo "======================"

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os

# Check models.py
with open('study_app/models.py', 'r') as f:
    content = f.read()

# Check if unique_together is present and correct
if "unique_together = ['module', 'verse_reference', 'question_text']" in content:
    print("✅ unique_together found in models.py")
    
    # Show the exact location
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'unique_together' in line:
            start = max(0, i-2)
            end = min(len(lines), i+2)
            print("📋 Context:")
            for j in range(start, end):
                print(f"   {j+1}: {lines[j]}")
            break
else:
    print("❌ unique_together NOT found in models.py")
    
    # Add it properly
    print("Adding unique_together...")
    lines = content.split('\n')
    updated_lines = []
    in_meta = False
    added = False
    
    for line in lines:
        updated_lines.append(line)
        if 'class Meta:' in line and 'QuizQuestion' in '\n'.join(updated_lines[-10:]):
            in_meta = True
        if in_meta and not added and (line.strip() == '' or 'class ' in line or 'def ' in line):
            updated_lines.insert(-1, '        unique_together = [\'module\', \'verse_reference\', \'question_text\']')
            added = True
    
    if added:
        with open('study_app/models.py', 'w') as f:
            f.write('\n'.join(updated_lines))
        print("✅ Added unique_together to models.py")
    else:
        print("❌ Could not add unique_together")
PYEOF
