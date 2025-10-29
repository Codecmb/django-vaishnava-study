"""
Bulk Questions Views - Matching your individual question style
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import QuizQuestion, QuizModule, Book

@login_required
def bulk_questions(request, book_id):
    """Bulk questions entry - matches individual question style"""
    book = get_object_or_404(Book, id=book_id)
    modules = QuizModule.objects.filter(course=book.course).order_by('order')
    
    context = {
        'book': book,
        'modules': modules,
    }
    return render(request, 'study_app/bulk_questions.html', context)

@login_required
def process_bulk_questions(request, book_id):
    """Process bulk questions submission"""
    if request.method == 'POST':
        try:
            book = get_object_or_404(Book, id=book_id)
            module_id = request.POST.get('module')
            chapter = request.POST.get('chapter', '')
            questions_text = request.POST.get('questions_text', '')
            
            if not module_id:
                messages.error(request, 'Please select a module')
                return redirect('bulk_questions', book_id=book_id)
            
            module = QuizModule.objects.get(id=module_id)
            
            # Parse questions
            lines = [line.strip() for line in questions_text.split('\n') if line.strip()]
            imported_count = 0
            
            for i, line in enumerate(lines):
                if not line:
                    continue
                    
                # Support multiple formats
                if '|' in line:
                    parts = line.split('|')
                    question_text = parts[0].strip()
                    verse = parts[1].strip() if len(parts) > 1 else ''
                    correct_answer = parts[2].strip() if len(parts) > 2 else ''
                    hint = parts[3].strip() if len(parts) > 3 else 'Study the verse carefully'
                else:
                    question_text = line
                    verse = ''
                    correct_answer = ''
                    hint = 'Study the verse carefully'
                
                if question_text:
                    # Auto-generate professional multiple choice
                    options = generate_professional_options(question_text, correct_answer)
                    
                    # If no correct answer provided, use the first option
                    if not correct_answer:
                        correct_answer = options[0]
                    
                    QuizQuestion.objects.create(
                        book=book,
                        module=module,
                        chapter=chapter,
                        question_text=question_text,
                        correct_answers=correct_answer,
                        verse_reference=verse,
                        additional_guidance=hint,
                        multiple_choice_options=json.dumps(options),
                        order=(imported_count + 1) * 10
                    )
                    imported_count += 1
            
            messages.success(request, f'✅ Successfully added {imported_count} questions to {module.name}!')
            return redirect('study_app:quiz_dashboard', book_id=book_id)
            
        except Exception as e:
            messages.error(request, f'❌ Error adding questions: {str(e)}')
            return redirect('bulk_questions', book_id=book_id)
    
    return redirect('study_app:quiz_dashboard', book_id=book_id)

def generate_professional_options(question_text, correct_answer):
    """Generate professional A/B/C/D options"""
    question_lower = question_text.lower()
    
    if not correct_answer:
        # Generate appropriate correct answer based on question
        if 'soul' in question_lower:
            correct_answer = "The soul is eternal, indestructible, and cannot be killed by any means"
        elif 'bhakti' in question_lower:
            correct_answer = "The process of devotional service to Lord Krishna"
        elif 'karma' in question_lower:
            correct_answer = "Material activities that bind the soul to the cycle of birth and death"
        elif 'krishna' in question_lower:
            correct_answer = "The Supreme Personality of Godhead"
        else:
            correct_answer = "The eternal nature of spiritual reality"
    
    # Generate distractors
    if 'soul' in question_lower:
        return [
            correct_answer,
            "The soul is temporary and perishes with the body",
            "The soul is a product of material energy",
            "The soul is an illusion created by the mind"
        ]
    elif 'bhakti' in question_lower:
        return [
            correct_answer,
            "A type of material meditation technique",
            "A method for economic development",
            "A form of mental speculation"
        ]
    elif 'karma' in question_lower:
        return [
            correct_answer,
            "A type of yoga for physical health",
            "The law of material attraction",
            "A system of government"
        ]
    else:
        return [
            correct_answer,
            "A temporary material manifestation",
            "A product of the material energy",
            "A form of illusion (maya)"
        ]
