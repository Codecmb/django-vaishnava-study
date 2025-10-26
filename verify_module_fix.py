#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import Book, QuizModule, QuizQuestion

print("✅ VERIFYING MODULE FIX")
print("=" * 40)

# Check book 1
book_1 = Book.objects.get(id=1)
print(f"📖 Book 1: {book_1.title}")
print(f"   Course: {book_1.course.name if book_1.course else 'None'}")

if book_1.course:
    modules = QuizModule.objects.filter(course=book_1.course)
    print(f"   Modules: {modules.count()}")
    
    for module in modules:
        questions = QuizQuestion.objects.filter(book=book_1, module=module)
        print(f"      📂 {module.name}: {questions.count()} questions")
        
        if questions.count() > 0:
            for q in questions:
                print(f"         ❓ {q.question_text[:50]}...")
                print(f"         ✅ MC Options: {len(q.get_multiple_choice_list())} choices")

print(f"\n🎯 TEST NOW:")
print(f"   http://127.0.0.1:8000/book/1/quiz/")
print(f"   Should show {modules.count()} modules with Take Quiz buttons")
