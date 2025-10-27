from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Book, QuizModule, QuizQuestion
from .forms import QuizQuestionForm
import json

def bulk_upload_questions(request, book_id, module_id):
    """Bulk upload questions with automatic choice generation"""
    book = get_object_or_404(Book, id=book_id)
    module = get_object_or_404(QuizModule, id=module_id)
    
    if request.method == 'POST':
        if 'questions_text' in request.POST:
            questions_text = request.POST['questions_text']
            questions_list = [q.strip() for q in questions_text.split('\\n') if q.strip()]
            
            created_count = 0
            for question_text in questions_list:
                question = QuizQuestion(
                    book=book,
                    module=module,
                    question_text=question_text,
                    chapter=request.POST.get('chapter', 'Chapter 1')
                )
                question.save()  # This will trigger the signal to generate choices
                created_count += 1
            
            messages.success(request, f'Successfully created {created_count} questions with auto-generated multiple choice options!')
            return redirect('study_app:quiz_dashboard', book_id=book_id)
    
    context = {
        'book': book,
        'module': module,
    }
    return render(request, 'study_app/bulk_upload_questions.html', context)
