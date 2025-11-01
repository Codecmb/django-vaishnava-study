#!/bin/bash
echo "🧹 CLEANING EXISTING DUPLICATES"
echo "==============================="

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion
from django.db.models import Count

print("🔍 Finding existing duplicates...")

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
        ).order_by('id')
        
        # Keep the first one, delete the rest
        keep = questions.first()
        to_delete = questions[1:]
        
        for q in to_delete:
            print(f"🗑️  Deleting duplicate: {q.question_text[:50]}...")
            q.delete()
            total_deleted += 1
    
    print(f"🎉 Deleted {total_deleted} duplicate questions")

# Final count
final_count = QuizQuestion.objects.count()
print(f"📊 Final question count: {final_count}")

# Verify no duplicates remain
final_duplicates = QuizQuestion.objects.values(
    'module', 'verse_reference', 'question_text'
).annotate(count=Count('id')).filter(count__gt=1)

if not final_duplicates:
    print("✅ No duplicates remain!")
else:
    print(f"❌ Still have {len(final_duplicates)} duplicate sets")
PYEOF

echo ""
echo "🧹 DUPLICATE CLEANUP COMPLETED!"
