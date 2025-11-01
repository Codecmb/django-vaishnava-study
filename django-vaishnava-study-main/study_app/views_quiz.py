from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from .models import Book, QuizModule, QuizQuestion, QuizAttempt
from .forms import QuizQuestionForm, QuizAnswerForm, QuizModuleForm

def quiz_dashboard(request, book_id):
    """Main quiz dashboard for a book"""
    book = get_object_or_404(Book, id=book_id)
    modules = QuizModule.objects.filter(course=book.course)
    
    context = {
        'book': book,
        'modules': modules,
    }
    return render(request, 'study_app/quiz_dashboard.html', context)

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
            request.session['latest_quiz_attempt'] = quiz_attempt.id
            
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
    
    # Get user answers with correctness
    user_answers = []
    for question in questions:
        user_answer = attempt.answers.get(str(question.id), '')
        is_correct = question.check_answer(user_answer)
        user_answers.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'correct_answers': question.get_correct_answers_list(),
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
        form = QuizQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.book = book
            question.save()
            messages.success(request, f'Successfully added quiz question for {book.title}')
            return redirect('study_app:quiz_dashboard', book_id=book_id)
    else:
        form = QuizQuestionForm(initial={'book': book})
    
    context = {
        'book': book,
        'form': form,
    }
    return render(request, 'study_app/add_quiz_question.html', context)

@login_required
def add_quiz_module(request, course_id):
    """Add a new quiz module (for adding more books later)"""
    from .models import Course
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = QuizModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, f'Successfully added quiz module for {course.name}')
            return redirect('admin:study_app_quizmodule_changelist')
    else:
        form = QuizModuleForm(initial={'course': course})
    
    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'study_app/add_quiz_module.html', context)
