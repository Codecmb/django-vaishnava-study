from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from .models import Book, QuizModule, QuizQuestion, QuizAttempt, BookPDF, Course
from .forms import QuizAnswerForm
from .pdf_commentary_service import pdf_commentary
from .book_based_evaluator import book_evaluator
import logging

logger = logging.getLogger(__name__)

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
            
            # Calculate score using book-based evaluation
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
    """Display quiz results with book-based evaluation and Prabhupada commentary"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    # Generate comprehensive evaluation results using book content
    evaluation_results = []
    answers = attempt.answers if attempt.answers else {}
    total_score = 0
    total_questions = len(answers)
    
    for qid, user_answer in answers.items():
        try:
            question = QuizQuestion.objects.get(id=int(qid))
            
            # Use book-based evaluation
            is_correct, feedback, commentary = book_evaluator.evaluate_answer(
                question=question.question_text,
                user_answer=user_answer,
                question_id=qid
            )
            
            score = 1 if is_correct else 0
            total_score += score
            
            evaluation_results.append({
                'question_id': qid,
                'question_text': question.question_text,
                'user_answer': user_answer,
                'correct_answer': question.correct_answers or "Based on Bhagavad-gita teachings",
                'is_correct': is_correct,
                'feedback': feedback,
                'commentary': commentary,
                'score': score,
                'max_score': 1,
                'chapter': getattr(question, 'chapter', 'General')
            })
            
        except Exception as e:
            logger.error(f"Error processing question {qid}: {e}")
            # Provide basic result even if processing fails
            evaluation_results.append({
                'question_id': qid,
                'question_text': f"Question {qid}",
                'user_answer': user_answer,
                'correct_answer': "Study Bhagavad-gita As It Is",
                'is_correct': len(user_answer.strip()) > 0,
                'feedback': "Continue your spiritual studies",
                'commentary': "Regular study of Srila Prabhupada's books will reveal the complete spiritual science.",
                'score': 1 if len(user_answer.strip()) > 0 else 0,
                'max_score': 1,
                'chapter': 'General'
            })
    
    # Calculate overall metrics
    percentage = (total_score / total_questions * 100) if total_questions > 0 else 0
    
    context = {
        'attempt': attempt,
        'results': evaluation_results,
        'total_score': total_score,
        'total_questions': total_questions,
        'percentage': percentage,
        'passed': percentage >= 70,
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
        chapter = request.POST.get('chapter', '')
        
        if module_id and question_text and correct_answers:
            module = QuizModule.objects.get(id=module_id)
            QuizQuestion.objects.create(
                book=book,
                module=module,
                chapter=chapter,
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
