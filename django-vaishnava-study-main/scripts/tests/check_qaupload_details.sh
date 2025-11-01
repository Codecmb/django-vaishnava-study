#!/bin/bash
echo "🔍 CHECKING QAUPLOAD DETAILS"
echo "============================"

cd ~/django-vaishnava-study
source venv/bin/activate

# Check the QAUpload model definition and any processing logic
python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

# Read the models.py to see QAUpload definition
print("📄 QAUpload model definition:")
with open('study_app/models.py', 'r') as f:
    content = f.read()
    # Find QAUpload class
    start = content.find('class QAUpload')
    if start != -1:
        end = content.find('class', start + 1)
        if end == -1:
            end = len(content)
        print(content[start:end])
    else:
        print("   QAUpload class not found in models.py")

# Check if there's a save method or processing logic
print("\n🔧 Checking for processing methods...")
from study_app.models import QAUpload
import inspect

# Get all methods of QAUpload
methods = inspect.getmembers(QAUpload, predicate=inspect.ismethod)
for name, method in methods:
    if not name.startswith('_'):
        print(f"  - {name}")

# Check if there's a process_csv method or similar
if hasattr(QAUpload, 'process_csv'):
    print("✅ Found process_csv method")
elif hasattr(QAUpload, 'save'):
    # Check if save method has processing logic
    source = inspect.getsource(QAUpload.save)
    if 'csv' in source.lower() or 'process' in source.lower():
        print("✅ Save method contains processing logic")
    else:
        print("ℹ️  Save method doesn't appear to process CSV")
else:
    print("ℹ️  No custom save method found")

PYEOF

# Check the admin configuration
echo ""
echo "🏛️  Checking QAUpload admin configuration..."
python3 << 'PYEOF'
import os

with open('study_app/admin.py', 'r') as f:
    content = f.read()
    
# Find QAUpload admin configuration
if 'QAUpload' in content:
    print("✅ QAUpload found in admin.py")
    # Extract the QAUpload admin section
    import re
    match = re.search(r'@admin\.register\(QAUpload\).*?class (\w+)\(.*?\):.*?(\n    .*?)*?(?=\n\n|\n@|\nclass|\Z)', content, re.DOTALL)
    if match:
        print("QAUpload Admin Class:")
        print(match.group(0)[:500])  # Print first 500 chars
    else:
        print("Could not extract QAUpload admin details")
else:
    print("❌ QAUpload not found in admin.py")
PYEOF
