"""
Paginated Quiz Views for Professional Test Format
"""

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import json

@login_required
def take_quiz_professional(request, book_id, module_id):
    """Professional quiz interface with pagination"""
    book = get_object_or_404(Book, id=book_id)
    module = get_object_or_404(QuizModule, id=module_id)
    questions = module.questions.all().order_by('order')
    
    # Prepare questions with multiple choice options
    for question in questions:
        if question.multiple_choice_options:
            try:
                question.multiple_choice_options_list = json.loads(question.multiple_choice_options)
            except:
                # If no multiple choice options, generate some
                question.multiple_choice_options_list = generate_multiple_choice(question)
        else:
            question.multiple_choice_options_list = generate_multiple_choice(question)
    
    # Pagination - 5 questions per page
    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'book': book,
        'module': module,
        'page_questions': page_obj,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else 1,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else paginator.num_pages,
        'progress_percentage': int((page_obj.number - 1) / paginator.num_pages * 100),
        'start_index': (page_obj.number - 1) * 5 + 1,
    }
    
    return render(request, 'study_app/take_quiz_professional.html', context)

def generate_multiple_choice(question):
    """Generate multiple choice options based on question content"""
    question_lower = question.question_text.lower()
    
    if 'soul' in question_lower or 'eternal' in question_lower:
        return [
            "The soul is eternal, indestructible, and cannot be killed by any means",
            "The soul is temporary and perishes with the body",
            "The soul is a product of material energy",
            "The soul is an illusion created by the mind"
        ]
    elif 'bhakti' in question_lower or 'devotional' in question_lower:
        return [
            "The process of devotional service to Lord Krishna",
            "A type of material meditation technique",
            "A method for economic development",
            "A form of mental speculation"
        ]
    elif 'karma' in question_lower:
        return [
            "Material activities that bind the soul to rebirth",
            "A type of yoga for physical health",
            "The law of material attraction",
            "A system of government"
        ]
    elif 'krishna' in question_lower:
        return [
            "The Supreme Personality of Godhead",
            "A great historical philosopher",
            "A mythical character from stories",
            "A symbol of nature"
        ]
    else:
        # Generic options for other questions
        return [
            "The eternal nature of spiritual reality",
            "A temporary material manifestation",
            "A product of the material energy",
            "A form of illusion (maya)"
        ]
