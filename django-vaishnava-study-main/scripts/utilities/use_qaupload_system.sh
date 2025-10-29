#!/bin/bash
echo "🚀 HOW TO USE QAUPLOAD FOR BULK UPLOADS"
echo "======================================"

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import Book

print("📋 AVAILABLE BOOKS FOR QAUPLOAD:")
books = Book.objects.all()
for book in books:
    print(f"  - {book.id}: {book.title}")

print(f"\n🎯 INSTRUCTIONS FOR BULK UPLOAD:")
print("1. Go to Django Admin → WASHNAVA STUDY → Qa uploads")
print("2. Click 'ADD QA UPLOAD +'")
print("3. Select a Book")
print("4. Upload a CSV file with questions")
print("5. Add any notes (optional)")
print("6. Save - the system should process the CSV automatically")

print(f"\n📝 EXPECTED CSV FORMAT:")
print("   The CSV should contain columns for quiz questions")
print("   Likely columns: chapter, verse_reference, question_text, etc.")
print("   Check the model or existing code for exact format")

print(f"\n💡 TROUBLESHOOTING:")
print("   - If processing doesn't happen automatically, check the QAUpload model")
print("   - Look for a process_csv() method or similar in models.py")
print("   - Check if there are any signals or background tasks")
print("   - The 'processed' field should change to True after successful upload")
PYEOF

# Let's also create a sample CSV template for bulk upload
echo ""
echo "📄 Creating sample CSV template..."
python3 << 'PYEOF'
import csv
import os

# Create a sample CSV template
sample_csv = 'qaupload_sample_template.csv'
with open(sample_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    # Based on QuizQuestion model fields
    writer.writerow(['chapter', 'verse_reference', 'question_text', 'correct_answers', 'additional_guidance', 'order'])
    writer.writerow(['Chapter 1', 'BG 1.1', 'What is the significance of Dhritarashtra\'s first question?', 'Curiosity about the battlefield, Attachment to his sons', 'Refer to Prabhupada commentary', '1'])
    writer.writerow(['Chapter 1', 'BG 1.2', 'Why did Duryodhana approach Dronacarya?', 'To boost morale, To show respect to guru', 'Study the military strategy', '2'])
    writer.writerow(['Chapter 2', 'BG 2.13', 'Explain the concept of soul transmigration.', 'Soul is eternal, Body changes like clothes', 'Bhagavad-gita verse 2.13 explanation', '1'])

print(f"✅ Created sample CSV template: {sample_csv}")
print("   You can use this as a starting point for your bulk uploads")
PYEOF
