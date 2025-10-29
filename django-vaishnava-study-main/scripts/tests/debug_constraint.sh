#!/bin/bash
echo "🐛 DEBUGGING UNIQUE CONSTRAINT ISSUE"
echo "===================================="

cd ~/django-vaishnava-study
source venv/bin/activate

# Check the actual database state
python3 << 'PYEOF'
import sqlite3
import os

db_path = 'db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔍 DATABASE SCHEMA INSPECTION:")

# Check table schema
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='study_app_quizquestion'")
table_sql = cursor.fetchone()
print("📋 Table SQL:")
print(table_sql[0] if table_sql else "No table found")

# Check indexes
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='study_app_quizquestion'")
indexes = cursor.fetchall()
print("\n📋 Indexes:")
for idx in indexes:
    print(f"   {idx[0]}: {idx[1]}")

conn.close()
PYEOF

# Check models.py content
echo ""
echo "🔍 MODELS.PY INSPECTION:"
python3 << 'PYEOF'
import os

with open('study_app/models.py', 'r') as f:
    content = f.read()

# Find the QuizQuestion Meta class
lines = content.split('\n')
in_meta = False
for i, line in enumerate(lines):
    if 'class QuizQuestion' in line:
        print("📋 QuizQuestion class found")
    if 'class Meta:' in line and 'QuizQuestion' in '\n'.join(lines[max(0,i-10):i]):
        in_meta = True
        print("📋 Meta class content:")
    if in_meta:
        print(f"   {line}")
        if line.strip() == '':
            break
PYEOF

# Check migration files
echo ""
echo "🔍 MIGRATION FILES:"
find study_app/migrations -name "*.py" -exec basename {} \; | sort
