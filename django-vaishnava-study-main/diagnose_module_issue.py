#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import Book, QuizModule, QuizQuestion

print("🔍 DIAGNOSING MODULE-BOOK RELATIONSHIP")
print("=" * 50)

# Check all books
books = Book.objects.all()
print(f"📚 Total books in database: {books.count()}")

for book in books:
    print(f"\n📖 Book {book.id}: {book.title}")
    print(f"   Course: {book.course.name if book.course else 'No course'}")
    
    # Check modules for this book's course
    if book.course:
        modules = QuizModule.objects.filter(course=book.course)
        print(f"   Modules for this course: {modules.count()}")
        
        for module in modules:
            questions = QuizQuestion.objects.filter(book=book, module=module)
            print(f"      📂 {module.name}: {questions.count()} questions")
    else:
        print("   ❌ Book has no course assigned!")

# Check which books actually have quiz modules
print(f"\n🎯 BOOKS WITH QUIZ MODULES:")
books_with_modules = []
for book in books:
    if book.course:
        modules = QuizModule.objects.filter(course=book.course)
        if modules.exists():
            books_with_modules.append(book)
            print(f"   ✅ Book {book.id}: {book.title}")

if not books_with_modules:
    print("   ❌ No books have quiz modules!")
    print("\n💡 PROBLEM: Modules exist but aren't linked to books via courses")
else:
    print(f"\n📊 Found {len(books_with_modules)} books with quiz modules")

# Show all quiz modules in the system
print(f"\n📋 ALL QUIZ MODULES IN SYSTEM:")
modules = QuizModule.objects.all()
for module in modules:
    questions = QuizQuestion.objects.filter(module=module)
    books_in_module = Book.objects.filter(course=module.course)
    print(f"   📂 {module.name} (Course: {module.course.name})")
    print(f"      Books: {books_in_module.count()}") 
    print(f"      Questions: {questions.count()}")
    for book in books_in_module:
        print(f"         - Book {book.id}: {book.title}")
