#!/bin/bash
echo "🧪 TESTING FIXED QAUPLOAD SYSTEM"
echo "================================"

cd ~/django-vaishnava-study
source venv/bin/activate

python3 << 'PYEOF'
import os
import sys
import django
from django.core.files.uploadedfile import SimpleUploadedFile

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QAUpload, Book, QuizQuestion
import csv
import io

print("🧪 Testing fixed QAUpload processing...")

# Get first book
book = Book.objects.first()
print(f"Using book: {book.title}")

# Create a proper CSV content with all required fields
csv_content = """chapter,verse_reference,question_text,correct_answers,additional_guidance,order
Chapter 1,BG 1.1,What is the significance of Dhritarashtra's first question?,Curiosity about the battlefield; Attachment to his sons,Refer to Prabhupada commentary,1
Chapter 1,BG 1.2,Why did Duryodhana approach Dronacarya?,To boost morale; To show respect to guru,Study the military strategy,2
Chapter 2,BG 2.13,Explain the concept of soul transmigration.,Soul is eternal; Body changes like clothes,Bhagavad-gita verse 2.13 explanation,1"""

# Create a file-like object
csv_file = SimpleUploadedFile(
    "test_bulk_upload.csv",
    csv_content.encode('utf-8'),
    content_type="text/csv"
)

print("📊 Before QAUpload:")
print(f"  - Total QuizQuestions: {QuizQuestion.objects.count()}")

# Create and save QAUpload instance (should auto-process)
try:
    qa_upload = QAUpload.objects.create(
        book=book,
        csv_file=csv_file,
        notes="Test bulk upload with processing"
    )
    
    print("✅ QAUpload created successfully")
    print(f"  - processed field: {qa_upload.processed}")
    print(f"  - notes: {qa_upload.notes}")
    
    # Check if questions were created
    print("📊 After QAUpload:")
    print(f"  - Total QuizQuestions: {QuizQuestion.objects.count()}")
    
    # Check questions for this book
    new_questions = QuizQuestion.objects.filter(book=book)
    print(f"  - Questions for {book.title}: {new_questions.count()}")
    
    if new_questions.exists():
        print("🎉 SUCCESS: Questions created from CSV!")
        print("📝 Created questions:")
        for q in new_questions.order_by('order'):
            print(f"    - Order {q.order}: {q.question_text[:60]}...")
    else:
        print("❌ No questions were created")
        print("💡 Check the processing logic")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test manual processing as well
print("\n🧪 Testing manual processing...")
try:
    # Create another upload but don't save (to test manual process_csv)
    csv_file2 = SimpleUploadedFile(
        "test_manual.csv",
        "chapter,verse_reference,question_text,correct_answers,order\nChapter 3,BG 3.1,Test manual processing question,Test answer,1".encode('utf-8'),
        content_type="text/csv"
    )
    
    qa_upload2 = QAUpload(
        book=book,
        csv_file=csv_file2,
        notes="Test manual processing"
    )
    qa_upload2.save()  # This should auto-process
    
    print(f"✅ Manual test - processed: {qa_upload2.processed}")
    print(f"   notes: {qa_upload2.notes}")
    
except Exception as e:
    print(f"❌ Manual test error: {e}")

# Clean up test data
print("\n🧹 Cleaning up test data...")
QAUpload.objects.filter(notes__contains="Test").delete()
# Keep the questions for verification, just remove the test upload records

print("✅ Test completed!")
PYEOF
