#!/bin/bash
echo "🔍 VERIFYING ADMIN FIX"
echo "======================"

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from django.contrib import admin
from study_app.models import QuizQuestion, QuizModule

print("📋 VERIFYING ADMIN CONFIGURATION:")

# Check QuizModuleAdmin
module_admin = admin.site._registry[QuizModule]
print(f"✅ QuizModuleAdmin:")
print(f"   - list_display: {getattr(module_admin, 'list_display', 'MISSING')}")
print(f"   - actions: {getattr(module_admin, 'actions', 'MISSING')}")
print(f"   - list_filter: {getattr(module_admin, 'list_filter', 'MISSING')}")
print(f"   - search_fields: {getattr(module_admin, 'search_fields', 'MISSING')}")

# Check QuizQuestionAdmin
question_admin = admin.site._registry[QuizQuestion]
print(f"✅ QuizQuestionAdmin:")
print(f"   - list_display: {getattr(question_admin, 'list_display', 'MISSING')}")
print(f"   - actions: {getattr(question_admin, 'actions', 'MISSING')}")
print(f"   - list_filter: {getattr(question_admin, 'list_filter', 'MISSING')}")
print(f"   - search_fields: {getattr(question_admin, 'search_fields', 'MISSING')}")
print(f"   - list_per_page: {getattr(question_admin, 'list_per_page', 'MISSING')}")

# Check if actions are callable
print("\n🛠️ CHECKING ACTION METHODS:")
if hasattr(module_admin, 'actions') and module_admin.actions:
    for action_name in module_admin.actions:
        action_func = getattr(module_admin, action_name, None)
        if action_func:
            print(f"   ✅ {action_name}: {getattr(action_func, 'short_description', 'No description')}")
        else:
            print(f"   ❌ {action_name}: Method not found")

if hasattr(question_admin, 'actions') and question_admin.actions:
    for action_name in question_admin.actions:
        action_func = getattr(question_admin, action_name, None)
        if action_func:
            print(f"   ✅ {action_name}: {getattr(action_func, 'short_description', 'No description')}")
        else:
            print(f"   ❌ {action_name}: Method not found")

print("\n🎯 WHAT YOU SHOULD SEE NOW:")
print("1. In 'Quiz modules':")
print("   - Checkboxes for bulk actions")
print("   - 'Action' dropdown with: 'Duplicate selected quizzes', 'Export questions to CSV', 'Delete selected objects'")
print("   - List shows: Title, Book, Questions count, Created at")
print("")
print("2. In 'Quiz questions':") 
print("   - Checkboxes for bulk actions")
print("   - 'Action' dropdown with: 'Delete duplicate questions', 'Delete selected objects'")
print("   - List shows: Question text, Verse reference, Module, Chapter, Order")
print("   - Search box at the top")
print("   - Filter options on the right")
print("")
print("3. Delete buttons on individual object pages")
PYEOF
