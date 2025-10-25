#!/bin/bash
echo "🔍 CHECKING ADMIN BULK ACTIONS"
echo "=============================="

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.admin import QuizModuleAdmin, QuizQuestionAdmin
from study_app.models import QuizModule, QuizQuestion

print("📋 QuizModuleAdmin actions:")
module_admin = QuizModuleAdmin(QuizModule, None)
if hasattr(module_admin, 'actions'):
    for action in module_admin.actions:
        print(f"   - {action}")
else:
    print("   No actions found")

print("\n📋 QuizQuestionAdmin actions:")
question_admin = QuizQuestionAdmin(QuizQuestion, None)
if hasattr(question_admin, 'actions'):
    for action in question_admin.actions:
        print(f"   - {action}")
else:
    print("   No actions found")

# Also check the actual admin file content
print("\n📄 Admin file bulk operations section:")
with open('study_app/admin.py', 'r') as f:
    content = f.read()
    # Find bulk operations section
    if 'Bulk Operations' in content:
        start = content.find('Bulk Operations')
        print(content[start:start+500])
    else:
        print("   No 'Bulk Operations' section found")
PYEOF
