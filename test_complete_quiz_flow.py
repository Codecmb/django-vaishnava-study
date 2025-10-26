#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import Book, QuizQuestion, QuizModule

print("🎯 TESTING COMPLETE QUIZ FLOW")
print("=" * 50)

# Check books with quizzes
books = Book.objects.filter(quiz_questions__isnull=False).distinct()
print(f"📚 Books with quizzes: {books.count()}")

for book in books:
    print(f"\n📖 {book.title}:")
    modules = QuizModule.objects.filter(course=book.course)
    
    for module in modules:
        questions = book.quiz_questions.filter(module=module)
        mc_questions = questions.filter(multiple_choice_options__isnull=False)
        
        print(f"   📂 {module.name}:")
        print(f"      Total questions: {questions.count()}")
        print(f"      Multiple choice: {mc_questions.count()}")
        
        if mc_questions.count() > 0:
            sample = mc_questions.first()
            options = sample.get_multiple_choice_list()
            print(f"      Sample: '{sample.question_text[:50]}...'")
            print(f"      Options: {len(options)} choices")
        else:
            print(f"      ❌ No multiple choice questions!")

print("\n🔗 TESTING URLs:")
for book in books[:2]:  # Test first 2 books
    print(f"   Book {book.id} ({book.title}):")
    print(f"      Quiz Dashboard: /book/{book.id}/quiz/")
    
    modules = QuizModule.objects.filter(course=book.course)[:2]
    for module in modules:
        if book.quiz_questions.filter(module=module).exists():
            print(f"      Take Quiz: /book/{book.id}/quiz/module/{module.id}/")

print("\n🎉 READY FOR TESTING!")
print("1. Start server: python3 manage.py runserver")
print("2. Visit: http://127.0.0.1:8000/book/1/quiz/")
print("3. Click 'Take This Quiz' buttons")
print("4. You should see multiple choice questions")
