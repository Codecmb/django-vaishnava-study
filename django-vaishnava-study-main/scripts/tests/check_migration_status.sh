#!/bin/bash
echo "🔍 CHECKING MIGRATION STATUS"
echo "============================"

cd ~/django-vaishnava-study
source venv/bin/activate

echo "📋 Current migration status:"
python manage.py showmigrations study_app

echo ""
echo "📊 Database status:"
python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from django.db import connection

# Check if unique constraint exists in database
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT name, sql FROM sqlite_master 
        WHERE type='index' AND tbl_name='study_app_quizquestion'
        AND sql LIKE '%UNIQUE%'
    """)
    unique_indexes = cursor.fetchall()
    
    print("✅ Database unique constraints:")
    for idx in unique_indexes:
        print(f"   - {idx[0]}: {idx[1]}")

# Check table counts
from study_app.models import QuizQuestion, QuizModule, QAUpload, Book
print(f"📊 Table counts:")
print(f"   - Books: {Book.objects.count()}")
print(f"   - QuizModules: {QuizModule.objects.count()}")
print(f"   - QuizQuestions: {QuizQuestion.objects.count()}")
print(f"   - QAUploads: {QAUpload.objects.count()}")
PYEOF
