def add_bulk_questions():
    # Read views.py
    with open('study_app/views.py', 'r') as f:
        content = f.read()
    
    # Add bulk questions function before the last function
    bulk_questions_code = '''
@login_required
def bulk_questions(request, book_id):
    """Bulk upload questions for a specific book"""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    from .models import Book, QuizModule, QuizQuestion
    
    book = get_object_or_404(Book, id=book_id)
    modules = QuizModule.objects.filter(course=book.course)
    
    if request.method == 'POST':
        module_id = request.POST.get('module')
        chapter = request.POST.get('chapter', 'Chapter 1')
        questions_text = request.POST.get('questions_text', '')
        
        if not module_id:
            messages.error(request, 'Please select a module')
        elif not questions_text.strip():
            messages.error(request, 'Please enter some questions')
        else:
            try:
                module = QuizModule.objects.get(id=module_id)
                
                # Parse questions (one per line)
                lines = [line.strip() for line in questions_text.split('\\n') if line.strip()]
                imported_count = 0
                existing_count = 0
                
                # Get current max order for this module
                max_order = QuizQuestion.objects.filter(module=module).aggregate(models.Max('order'))['order__max'] or 0
                
                for i, question_text in enumerate(lines, 1):
                    if not question_text:
                        continue
                        
                    # Skip if question already exists (case insensitive partial match)
                    if QuizQuestion.objects.filter(
                        module=module, 
                        question_text__icontains=question_text[:50]
                    ).exists():
                        existing_count += 1
                        continue
                    
                    QuizQuestion.objects.create(
                        book=book,
                        module=module,
                        chapter=chapter,
                        question_text=question_text,
                        order=max_order + i,
                        additional_guidance="Study relevant scriptures"
                    )
                    imported_count += 1
                
                if imported_count > 0:
                    messages.success(request, f'Successfully imported {imported_count} questions to {module.name}!')
                if existing_count > 0:
                    messages.warning(request, f'Skipped {existing_count} duplicate questions')
                    
                return redirect('study_app:quiz_dashboard', book_id=book_id)
                
            except Exception as e:
                messages.error(request, f'Error importing questions: {str(e)}')
    
    context = {
        'book': book,
        'modules': modules,
    }
    return render(request, 'study_app/bulk_questions.html', context)
'''
    
    # Insert before the last function
    import re
    pattern = r'(def enhance_quiz_dashboard\(\):.*?)(\Z)'
    replacement = r'\\1' + bulk_questions_code + r'\\n\\2'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open('study_app/views.py', 'w') as f:
        f.write(new_content)
    
    print("Added bulk_questions function to views.py")

add_bulk_questions()
