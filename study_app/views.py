from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
from .models import Course, Book, QuestionAnswer

def index(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'vaishnava_study/index.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    books = course.books.all()
    
    context = {
        'course': course,
        'books': books,
    }
    return render(request, 'vaishnava_study/course_detail.html', context)

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    qas = book.qas.all()
    
    context = {
        'book': book,
        'qas': qas,
    }
    return render(request, 'vaishnava_study/book_detail.html', context)

def qa_section(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    qas = book.qas.all()
    
    context = {
        'book': book,
        'qas': qas,
    }
    return render(request, 'vaishnava_study/qa_section.html', context)
