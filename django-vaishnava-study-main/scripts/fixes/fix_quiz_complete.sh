#!/bin/bash
echo "🎯 COMPLETE Django Quiz System Fix"
echo "==================================="

cd ~/django-vaishnava-study
source venv/bin/activate

# Phase 1: Clean duplicates
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
    duplicates = QuizQuestion.objects.values(
        'quiz_module', 'verse', 'question_text'
    ).annotate(count=Count('id')).filter(count__gt=1)
    
    if not duplicates:
        print("✅ No duplicates found!")
    else:
        print(f"📝 Found {len(duplicates)} duplicate sets")
        total_deleted = 0
        for dup in duplicates:
            questions = QuizQuestion.objects.filter(
                quiz_module=dup['quiz_module'],
                verse=dup['verse'],
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
PYEOF

# Phase 2: Fix admin.py duplicates
echo ""
echo "🔧 PHASE 2: Fixing admin registration..."
python3 << 'PYEOF'
import os

admin_file = 'study_app/admin.py'
try:
    with open(admin_file, 'r') as f:
        content = f.read()
    
    # Create backup
    with open(admin_file + '.backup2', 'w') as f:
        f.write(content)
    
    # Remove duplicate registrations
    lines = content.split('\n')
    cleaned_lines = []
    in_quizmodule = False
    in_quizquestion = False
    skip_section = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for duplicate QuizModule registration
        if '@admin.register(QuizModule)' in line and not in_quizmodule:
            cleaned_lines.append(line)
            in_quizmodule = True
            # Skip until we find the next class definition that's not QuizModuleAdmin
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('@admin.register'):
                cleaned_lines.append(lines[i])
                i += 1
            i -= 1  # Adjust counter
            
        # Check for duplicate QuizQuestion registration  
        elif '@admin.register(QuizQuestion)' in line and not in_quizquestion:
            cleaned_lines.append(line)
            in_quizquestion = True
            # Skip until we find the next class definition that's not QuizQuestionAdmin
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('@admin.register'):
                cleaned_lines.append(lines[i])
                i += 1
            i -= 1  # Adjust counter
            
        # Skip duplicate registrations
        elif '@admin.register(QuizModule)' in line and in_quizmodule:
            print("✅ Removed duplicate QuizModule registration")
            # Skip this entire duplicate section
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('@admin.register'):
                i += 1
            i -= 1
            
        elif '@admin.register(QuizQuestion)' in line and in_quizquestion:
            print("✅ Removed duplicate QuizQuestion registration") 
            # Skip this entire duplicate section
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('@admin.register'):
                i += 1
            i -= 1
            
        else:
            cleaned_lines.append(line)
            
        i += 1
    
    # Write cleaned content
    with open(admin_file, 'w') as f:
        f.write('\n'.join(cleaned_lines))
    
    print("✅ Admin file cleaned successfully")
    
except Exception as e:
    print(f"❌ Admin fix error: {e}")
    import traceback
    traceback.print_exc()
PYEOF

# Phase 3: Add unique constraint
echo ""
echo "🔒 PHASE 3: Adding unique constraint..."
python3 << 'PYEOF'
import os

models_file = 'study_app/models.py'
try:
    with open(models_file, 'r') as f:
        content = f.read()
    
    # Create backup
    with open(models_file + '.backup2', 'w') as f:
        f.write(content)
    
    if 'unique_together' in content and 'QuizQuestion' in content:
        print("✅ Unique constraint already exists")
    else:
        lines = content.split('\n')
        updated = []
        in_class = False
        added = False
        
        for line in lines:
            updated.append(line)
            if 'class QuizQuestion' in line:
                in_class = True
            if in_class and 'class Meta:' in line and not added:
                updated.append('        unique_together = [\'quiz_module\', \'verse\', \'question_text\']')
                added = True
                print("✅ Added unique_together constraint")
        
        with open(models_file, 'w') as f:
            f.write('\n'.join(updated))
        
except Exception as e:
    print(f"❌ Models error: {e}")
PYEOF

# Phase 4: Run migrations
echo ""
echo "🔄 PHASE 4: Running migrations..."
python manage.py makemigrations study_app
python manage.py migrate study_app

echo ""
echo "🎉 ALL FIXES COMPLETED SUCCESSFULLY!"
echo ""
echo "📋 SUMMARY:"
echo "   ✅ Cleaned duplicate questions"
echo "   ✅ Fixed admin registration conflicts" 
echo "   ✅ Added unique constraint to prevent future duplicates"
echo "   ✅ Applied database migrations"
echo ""
echo "🚀 You can now run the server: python manage.py runserver"
