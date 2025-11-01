#!/bin/bash
echo "🔄 CREATING MIGRATIONS FOR UNIQUE CONSTRAINT"
echo "============================================"

cd ~/django-vaishnava-study
source venv/bin/activate

# Step 1: Make sure the unique_together is correctly added
python3 << 'PYEOF'
import os

models_file = 'study_app/models.py'
with open(models_file, 'r') as f:
    content = f.read()

# Check if unique_together is present
if "unique_together = ['module', 'verse_reference', 'question_text']" in content:
    print("✅ unique_together constraint found in models.py")
else:
    print("❌ unique_together constraint NOT found in models.py")
    print("Adding it now...")
    
    lines = content.split('\n')
    updated_lines = []
    in_quizquestion = False
    added = False
    
    for line in lines:
        updated_lines.append(line)
        
        if 'class QuizQuestion' in line:
            in_quizquestion = True
            
        if in_quizquestion and 'class Meta:' in line and not added:
            # Add the unique_together line after class Meta:
            updated_lines.append('        unique_together = [\'module\', \'verse_reference\', \'question_text\']')
            added = True
            print("✅ Added unique_together constraint")
            
        if in_quizquestion and line.strip() == '' and not added:
            # If no Meta class found, add one
            updated_lines.append('    class Meta:')
            updated_lines.append('        unique_together = [\'module\', \'verse_reference\', \'question_text\']')
            added = True
            print("✅ Added Meta class with unique_together constraint")
    
    if added:
        with open(models_file, 'w') as f:
            f.write('\n'.join(updated_lines))
        print("✅ Updated models.py successfully")
    else:
        print("❌ Could not add unique_together constraint")
PYEOF

# Step 2: Create migrations
echo ""
echo "🔄 Creating migrations..."
python manage.py makemigrations study_app

# Step 3: Apply migrations
echo ""
echo "🔄 Applying migrations..."
python manage.py migrate study_app

# Step 4: Verify the migration worked
echo ""
echo "✅ Verifying migration..."
python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion

try:
    # Test the unique constraint by trying to create a duplicate
    existing = QuizQuestion.objects.first()
    if existing:
        print("Testing unique constraint...")
        duplicate = QuizQuestion(
            module=existing.module,
            verse_reference=existing.verse_reference, 
            question_text=existing.question_text,
            chapter=existing.chapter
        )
        try:
            duplicate.save()
            print("❌ UNIQUE CONSTRAINT FAILED: Duplicate was created")
            duplicate.delete()
        except Exception as e:
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                print("✅ UNIQUE CONSTRAINT WORKING: Prevents duplicates")
            else:
                print(f"⚠️  Different error: {e}")
    else:
        print("ℹ️  No questions to test with")
        
except Exception as e:
    print(f"❌ Test error: {e}")
PYEOF

echo ""
echo "🎉 MIGRATION PROCESS COMPLETED!"
