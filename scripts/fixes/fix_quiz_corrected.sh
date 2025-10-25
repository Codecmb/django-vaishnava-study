#!/bin/bash
echo "🎯 CORRECTED Django Quiz System Fix"
echo "===================================="

cd ~/django-vaishnava-study
source venv/bin/activate

# Phase 1: Clean duplicates with correct field names
echo ""
echo "🔍 PHASE 1: Cleaning duplicate questions..."
python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

try:
    django.setup()
    from study_app.models import QuizQuestion
    from django.db.models import Count
    
    print("Searching for duplicate questions...")
    # Using the correct field names: module (not quiz_module) and verse_reference (not verse)
    duplicates = QuizQuestion.objects.values(
        'module', 'verse_reference', 'question_text'
    ).annotate(count=Count('id')).filter(count__gt=1)
    
    if not duplicates:
        print("✅ No duplicates found!")
    else:
        print(f"📝 Found {len(duplicates)} duplicate sets")
        total_deleted = 0
        for dup in duplicates:
            questions = QuizQuestion.objects.filter(
                module=dup['module'],
                verse_reference=dup['verse_reference'],
                question_text=dup['question_text']
            )
            keep = questions.first()
            deleted = questions.count() - 1
            questions.exclude(pk=keep.pk).delete()
            total_deleted += deleted
            print(f"   Kept 1, deleted {deleted} - {keep.question_text[:50]}...")
        print(f"🎉 Deleted {total_deleted} total duplicates")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
PYEOF

# Phase 2: Fix the unique constraint in models.py
echo ""
echo "🔒 PHASE 2: Fixing unique constraint with correct field names..."
python3 << 'PYEOF'
import os

models_file = 'study_app/models.py'
try:
    with open(models_file, 'r') as f:
        content = f.read()
    
    # Create backup
    with open(models_file + '.backup3', 'w') as f:
        f.write(content)
    
    # Remove the incorrect unique_together and add correct one
    lines = content.split('\n')
    updated_lines = []
    in_quiz_question = False
    meta_found = False
    
    for line in lines:
        # Skip the incorrect unique_together line
        if "unique_together = ['quiz_module', 'verse', 'question_text']" in line:
            print("✅ Removing incorrect unique_together")
            continue
            
        updated_lines.append(line)
        
        if 'class QuizQuestion' in line:
            in_quiz_question = True
            
        if in_quiz_question and 'class Meta:' in line:
            meta_found = True
            
        # Add correct unique_together after class Meta
        if meta_found and ']' in line and 'unique_together' not in content:
            updated_lines.append('        unique_together = [\'module\', \'verse_reference\', \'question_text\']')
            print("✅ Added correct unique_together constraint")
            meta_found = False
            in_quiz_question = False
    
    # Write updated content
    with open(models_file, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print("✅ Models file updated with correct field names")
    
except Exception as e:
    print(f"❌ Models error: {e}")
    import traceback
    traceback.print_exc()
PYEOF

# Phase 3: Create and run migrations
echo ""
echo "🔄 PHASE 3: Creating and applying migrations..."
python manage.py makemigrations study_app
python manage.py migrate study_app

# Phase 4: Verify the fix
echo ""
echo "✅ PHASE 4: Verifying the fix..."
python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

try:
    django.setup()
    from study_app.models import QuizQuestion
    
    # Test that Django starts without errors
    print("✅ Django starts successfully")
    
    # Check unique constraint
    from django.db.models import Count
    duplicates = QuizQuestion.objects.values(
        'module', 'verse_reference', 'question_text'
    ).annotate(count=Count('id')).filter(count__gt=1)
    
    if not duplicates:
        print("✅ No duplicates remain in database")
    else:
        print(f"⚠️  {len(duplicates)} duplicates still exist")
        
    print(f"📊 Total questions in database: {QuizQuestion.objects.count()}")
    
except Exception as e:
    print(f"❌ Verification error: {e}")
PYEOF

echo ""
echo "🎉 FIXES COMPLETED WITH CORRECT FIELD NAMES!"
echo ""
echo "📋 CORRECTED FIELD MAPPING:"
echo "   - quiz_module → module"
echo "   - verse → verse_reference"
echo "   - question_text → question_text (same)"
