#!/bin/bash
echo "🔍 VERIFYING UNIQUE CONSTRAINT"
echo "=============================="

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os
import sys
import django
import sqlite3

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion
from django.db import IntegrityError

print("1. CHECKING DATABASE CONSTRAINTS:")
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check all constraints and indexes
cursor.execute("""
    SELECT name, sql FROM sqlite_master 
    WHERE tbl_name='study_app_quizquestion' AND (sql LIKE '%UNIQUE%' OR type='index')
""")
constraints = cursor.fetchall()

print("📋 Database constraints and indexes:")
for const in constraints:
    print(f"   {const[0]}: {const[1]}")

conn.close()

print("\n2. CHECKING DJANGO MODEL:")
from study_app.models import QuizQuestion
meta = QuizQuestion._meta
print(f"   unique_together: {getattr(meta, 'unique_together', 'NOT SET')}")

print("\n3. TESTING DUPLICATE PREVENTION:")
# Count duplicates before
from django.db.models import Count
duplicates_before = QuizQuestion.objects.values(
    'module', 'verse_reference', 'question_text'
).annotate(count=Count('id')).filter(count__gt=1)

print(f"   Current duplicate sets: {len(duplicates_before)}")

# Try to create a duplicate via ORM
existing = QuizQuestion.objects.first()
if existing:
    duplicate = QuizQuestion(
        book=existing.book,
        module=existing.module,
        chapter=existing.chapter,
        verse_reference=existing.verse_reference,
        question_text=existing.question_text,
        additional_guidance="Test",
        order=999
    )
    
    try:
        duplicate.save()
        print("   ❌ ORM: Could create duplicate")
        duplicate.delete()
    except IntegrityError:
        print("   ✅ ORM: Prevents duplicates")
    except Exception as e:
        print(f"   ⚠️  ORM: {e}")

print("\n4. CHECKING MIGRATION STATUS:")
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM django_migrations WHERE app='study_app' ORDER BY applied DESC LIMIT 3")
    recent_migrations = cursor.fetchall()
    print("   Recent migrations:")
    for mig in recent_migrations:
        print(f"     - {mig[0]}")

print("\n🎯 VERIFICATION COMPLETE!")
PYEOF
