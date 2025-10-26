#!/usr/bin/env python3
import os

print("🔗 ADDING QUIZ LINKS TO COURSE PAGES")
print("=" * 50)

# First, let's check the current book_detail template
book_detail_file = 'study_app/templates/study_app/book_detail.html'

if os.path.exists(book_detail_file):
    with open(book_detail_file, 'r') as f:
        content = f.read()
    
    # Check if quiz link already exists
    if 'quiz_dashboard' in content:
        print("✅ Quiz link already exists in book_detail.html")
    else:
        print("❌ No quiz link found in book_detail.html")
        print("💡 Need to add quiz access point")
else:
    print("❌ book_detail.html not found")

# Check course_detail template too
course_detail_file = 'study_app/templates/study_app/course_detail.html'
if os.path.exists(course_detail_file):
    with open(course_detail_file, 'r') as f:
        content = f.read()
    if 'quiz' in content.lower():
        print("✅ Quiz references found in course_detail.html")
    else:
        print("❌ No quiz references in course_detail.html")
else:
    print("❌ course_detail.html not found")

print("\n📊 RECOMMENDED ACTIONS:")
print("1. Add 'Take Quiz' button to book detail pages")
print("2. Show quiz availability on course pages") 
print("3. Make quizzes more discoverable in navigation")

print("\n🔗 Current quiz URLs that work:")
print("   http://127.0.0.1:8000/book/1/quiz/")
print("   http://127.0.0.1:8000/book/5/quiz/")
print("   http://127.0.0.1:8000/book/11/quiz/")
