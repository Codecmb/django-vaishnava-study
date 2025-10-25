#!/bin/bash
echo "🎯 FINAL COMPREHENSIVE FIX"
echo "=========================="

cd ~/django-vaishnava-study
source venv/bin/activate

# Step 1: Clean up any broken migrations
echo "1. Cleaning up migrations..."
find study_app/migrations -name "0000_*" -delete
find study_app/migrations -name "*add_unique_constraint*" -delete

# Step 2: Verify models.py
echo "2. Verifying models.py..."
python3 << 'PYEOF'
import os

with open('study_app/models.py', 'r') as f:
    content = f.read()

if "unique_together = ['module', 'verse_reference', 'question_text']" not in content:
    print("Adding unique_together to models.py...")
    # Simple sed approach
    os.system('sed -i \'/class Meta:/a\\\\        unique_together = [\\\"module\\\", \\\"verse_reference\\\", \\\"question_text\\\"]\' study_app/models.py')
PYEOF

# Step 3: Create and apply migration
echo "3. Creating migration..."
python manage.py makemigrations study_app --name add_unique_constraint

echo "4. Applying migration..."
python manage.py migrate study_app

# Step 4: Final test
echo "5. Final test..."
python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion
from django.db import IntegrityError

print("🧪 FINAL UNIQUE CONSTRAINT TEST")

existing = QuizQuestion.objects.first()
if existing:
    print(f"Testing with: {existing.question_text[:50]}...")
    
    duplicate = QuizQuestion(
        book=existing.book,
        module=existing.module,
        chapter=existing.chapter,
        verse_reference=existing.verse_reference,
        question_text=existing.question_text,
        order=999
    )
    
    try:
        duplicate.save()
        print("❌ FAILED: Unique constraint not working")
        duplicate.delete()
    except IntegrityError:
        print("✅ SUCCESS: Unique constraint is working!")
    except Exception as e:
        print(f"⚠️  Unexpected error: {e}")
else:
    print("ℹ️  No questions to test with")

print(f"📊 Total questions: {QuizQuestion.objects.count()}")
PYEOF

echo ""
echo "🎉 COMPREHENSIVE FIX COMPLETED!"
