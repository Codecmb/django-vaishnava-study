#!/bin/bash
echo "🔧 PROPERLY FIXING MODELS.PY"
echo "============================"

cd ~/django-vaishnava-study
source venv/bin/activate

# Step 1: Properly add unique_together to the existing Meta class
python3 << 'PYEOF'
import os

models_file = 'study_app/models.py'
with open(models_file, 'r') as f:
    content = f.read()

print("📝 Current models.py structure check...")

# Find where to insert unique_together
lines = content.split('\n')
updated_lines = []
meta_found = False
unique_added = False

for i, line in enumerate(lines):
    updated_lines.append(line)
    
    # Look for the Meta class inside QuizQuestion
    if 'class Meta:' in line:
        # Check if this is in QuizQuestion by looking back
        context = '\n'.join(lines[max(0, i-20):i+1])
        if 'class QuizQuestion' in context:
            meta_found = True
            print("✅ Found QuizQuestion Meta class")
    
    # If we're in Meta class and hit a blank line or next class, add unique_together
    if meta_found and not unique_added:
        if i+1 >= len(lines) or lines[i+1].strip() == '' or lines[i+1].startswith('    def ') or lines[i+1].startswith('class '):
            updated_lines.append('        unique_together = [\'module\', \'verse_reference\', \'question_text\']')
            unique_added = True
            print("✅ Added unique_together to Meta class")

if not meta_found:
    print("❌ Could not find QuizQuestion Meta class")
elif not unique_added:
    print("❌ Could not add unique_together")

# Write the updated content
with open(models_file, 'w') as f:
    f.write('\n'.join(updated_lines))

print("✅ Models.py updated")
PYEOF

# Step 2: Force migration creation
echo ""
echo "🔄 Forcing migration creation..."
python manage.py makemigrations study_app --name add_unique_constraint

# Step 3: Apply migration
echo ""
echo "🔄 Applying migration..."
python manage.py migrate study_app

# Step 4: Test the constraint properly
echo ""
echo "🧪 Testing unique constraint..."
python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, QuizModule, Book

try:
    # Get existing objects to test with
    existing = QuizQuestion.objects.first()
    if existing:
        print("Testing unique constraint with proper data...")
        
        # Create a proper duplicate with all required fields
        duplicate = QuizQuestion(
            book=existing.book,
            module=existing.module,
            chapter=existing.chapter,
            verse_reference=existing.verse_reference,
            question_text=existing.question_text,
            order=999  # Different order to avoid other constraints
        )
        
        try:
            duplicate.save()
            print("❌ UNIQUE CONSTRAINT FAILED: Duplicate was created")
            duplicate.delete()
        except Exception as e:
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                print("✅ UNIQUE CONSTRAINT WORKING: Prevents duplicates")
            else:
                print(f"⚠️  Error (might be different constraint): {e}")
    else:
        print("ℹ️  No questions to test with")
        
except Exception as e:
    print(f"❌ Test error: {e}")
    import traceback
    traceback.print_exc()
PYEOF

echo ""
echo "🎉 MODELS FIX COMPLETED!"
