#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import Book, QuizModule

print("📚 TESTING STUDENT QUIZ ACCESS")
print("=" * 40)

# Check what books have quizzes
books_with_quizzes = Book.objects.filter(quiz_questions__isnull=False).distinct()
print(f"Books with quizzes: {books_with_quizzes.count()}")

for book in books_with_quizzes:
    modules = QuizModule.objects.filter(course=book.course)
    print(f"\n📖 {book.title}:")
    for module in modules:
        questions_count = book.quiz_questions.filter(module=module).count()
        print(f"   - {module.name}: {questions_count} questions")

print("\n🔗 Student-accessible quiz URLs:")
books = Book.objects.all()[:3]  # Show first 3 books
for book in books:
    print(f"   /book/{book.id}/quiz/")

print("\n💡 To test: Start server and visit above URLs")
print("   python3 manage.py runserver")
print("   Then visit: http://127.0.0.1:8000/book/[book_id]/quiz/")
