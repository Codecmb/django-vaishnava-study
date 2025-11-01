#!/bin/bash
echo "🔍 EXAMINING QAUPLOAD PROCESSING LOGIC"
echo "======================================"

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os
import sys
import django
import inspect

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QAUpload

print("📄 QAUpload save method source code:")
try:
    source = inspect.getsource(QAUpload.save)
    print(source)
except Exception as e:
    print(f"❌ Could not get source: {e}")

# Let's check if there are any other processing methods
print("\n🔧 All QAUpload methods:")
for name, method in inspect.getmembers(QAUpload, predicate=inspect.ismethod):
    if not name.startswith('_'):
        print(f"  - {name}")
        try:
            # Try to get source for non-builtin methods
            if 'QAUpload' in str(method):
                source = inspect.getsource(method)
                if len(source) < 1000:  # Don't print huge methods
                    print(f"    Source: {source[:200]}...")
        except:
            pass

# Check if there's a process_csv method specifically
if hasattr(QAUpload, 'process_csv'):
    print("✅ Found process_csv method")
    try:
        source = inspect.getsource(QAUpload.process_csv)
        print(source)
    except Exception as e:
        print(f"❌ Could not get source: {e}")
else:
    print("ℹ️  No process_csv method found")
PYEOF
