from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from .models import Book, QuizModule, QuizQuestion, QuizAttempt
from .forms import QuizAnswerForm
from study_app.ai_service import get_ai_feedback

@login_required
def quiz_dashboard(request, book_id):
    """Show available quiz modules for a book"""
    book = get_object_or_404(Book, id=book_id)
    modules = QuizModule.objects.filter(course=book.course)
    
    # Get user's recent attempts
    recent_attempts = QuizAttempt.objects.filter(
        user=request.user, 
        book=book
    ).order_by('-completed_at')[:5]
    
    context = {
        'book': book,
        'modules': modules,
        'recent_attempts': recent_attempts,
    }
    return render(request, 'study_app/quiz_dashboard.html', context)

@login_required
def take_quiz(request, book_id, module_id):
    """Take a quiz for a specific module"""
    book = get_object_or_404(Book, id=book_id)
    module = get_object_or_404(QuizModule, id=module_id)
    questions = QuizQuestion.objects.filter(book=book, module=module).order_by('order')
    
    if not questions.exists():
        messages.warning(request, f'No quiz questions available for {module.name} yet.')
        return redirect('study_app:quiz_dashboard', book_id=book_id)
    
    if request.method == 'POST':
        form = QuizAnswerForm(request.POST, questions=questions)
        if form.is_valid():
            # Process quiz answers
            answers = {}
            for question in questions:
                answer_key = f'question_{question.id}'
                answers[str(question.id)] = form.cleaned_data.get(answer_key, '')
            
            # Create quiz attempt
            quiz_attempt = QuizAttempt.objects.create(
                user=request.user if request.user.is_authenticated else None,
                book=book,
                module=module,
                answers=answers
            )
            
            # Calculate score
            score = quiz_attempt.calculate_score()
            
            # Store attempt ID in session for results page
            request.session['last_quiz_attempt'] = quiz_attempt.id
            
            messages.success(request, f'Quiz completed! Your score: {score}/{len(questions)}')
            return redirect('study_app:quiz_results', attempt_id=quiz_attempt.id)
    else:
        form = QuizAnswerForm(questions=questions)
    
    context = {
        'book': book,
        'module': module,
        'questions': questions,
        'form': form,
    }
    return render(request, 'study_app/take_quiz.html', context)

def quiz_results(request, attempt_id):
    """Show quiz results with feedback"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    questions = QuizQuestion.objects.filter(module=attempt.module, book=attempt.book)
    
    # Get user answers with correctness and AI feedback
    user_answers = []
    for question in questions:
        user_answer_raw = attempt.answers.get(str(question.id), '')
        
        # Convert choice index to display text
        user_answer_display = user_answer_raw
        if user_answer_raw.isdigit():
            try:
                choices = question.get_choices_list()
                choice_index = int(user_answer_raw)
                if 0 <= choice_index < len(choices):
                    user_answer_display = choices[choice_index]
            except:
                pass
        
        is_correct = question.check_answer(user_answer_raw)
        correct_answers_list = question.get_correct_answers_list()
        
        # Generate AI feedback
        ai_feedback = get_ai_feedback(
            question_text=question.question_text,
            user_answer=user_answer_display,
            correct_answers=', '.join(correct_answers_list) if correct_answers_list else question.correct_answers,
            verse_reference=question.verse_reference
        )
        
        user_answers.append({
            'question': question,
            'user_answer': user_answer_display,
            'is_correct': is_correct,
            'correct_answers': correct_answers_list,
            'prabhupada_commentary': ai_feedback['prabhupada_commentary'],
            'additional_guidance': ai_feedback['additional_guidance'],
            'verse_reference': question.verse_reference,
        })
    
    context = {
        'attempt': attempt,
        'user_answers': user_answers,
        'feedback': attempt.get_feedback(),
    }
    return render(request, 'study_app/quiz_results.html', context)

@login_required
def add_quiz_question(request, book_id):
    """Add a new quiz question (admin function)"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # Process form data and create question
        module_id = request.POST.get('module')
        question_text = request.POST.get('question_text')
        correct_answers = request.POST.get('correct_answers')
        multiple_choice_options = request.POST.get('multiple_choice_options')
        
        if module_id and question_text and correct_answers:
            module = QuizModule.objects.get(id=module_id)
            QuizQuestion.objects.create(
                book=book,
                module=module,
                question_text=question_text,
                correct_answers=correct_answers,
                multiple_choice_options=multiple_choice_options,
            )
            messages.success(request, 'Quiz question added successfully!')
            return redirect('study_app:book_detail', book_id=book_id)
    
    modules = QuizModule.objects.filter(course=book.course)
    context = {
        'book': book,
        'modules': modules,
    }
    return render(request, 'study_app/add_quiz_question.html', context)

@login_required
def add_quiz_module(request, course_id):
    """Add a new quiz module (admin function)"""
    from .models import Course, QuizModule
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        chapters_range = request.POST.get('chapters_range')
        
        if name and chapters_range:
            QuizModule.objects.create(
                course=course,
                name=name,
                description=description,
                chapters_range=chapters_range
            )
            messages.success(request, 'Quiz module added successfully!')
            return redirect('study_app:course_detail', course_id=course_id)
    
    context = {
        'course': course,
    }
    return render(request, 'study_app/add_quiz_module.html', context)

@login_required
def quiz_question_management(request, book_id):
    """Manage quiz questions for a book"""
    book = get_object_or_404(Book, id=book_id)
    questions = QuizQuestion.objects.filter(book=book)
    
    context = {
        'book': book,
        'questions': questions,
    }
    return render(request, 'study_app/quiz_question_management.html', context)

@login_required 
def delete_quiz_question(request, question_id):
    """Delete a quiz question"""
    question = get_object_or_404(QuizQuestion, id=question_id)
    book_id = question.book.id
    question.delete()
    messages.success(request, 'Quiz question deleted successfully!')
    return redirect('study_app:quiz_question_management', book_id=book_id)
