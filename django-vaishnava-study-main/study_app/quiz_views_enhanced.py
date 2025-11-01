"""
Enhanced Quiz Views with Certificate System
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import QuizModule, QuizQuestion, QuizAttempt, Book
from .quiz_certificate_system import quiz_system

@login_required
def submit_quiz_complete(request, book_id, module_id):
    """Process quiz submission with auto-population and certificate generation"""
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        module = get_object_or_404(QuizModule, id=module_id)
        
        # Create quiz attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz_module=module,
            book=book
        )
        
        # Process student answers
        student_answers = {}
        for key, value in request.POST.items():
            if key.startswith('question_') and not key.endswith('_type'):
                question_id = key.split('_')[1]
                
                if key.endswith('_mc') and value:  # Multiple choice
                    student_answers[question_id] = {
                        'answer': value,
                        'type': 'multiple_choice'
                    }
                elif key.endswith('_written') and value.strip():  # Written
                    student_answers[question_id] = {
                        'answer': value.strip(),
                        'type': 'written'
                    }
        
        # Process complete quiz with auto-population and certificate
        result = quiz_system.process_quiz_completion(attempt, student_answers)
        
        if result['success']:
            # Store certificate data in session for results page
            request.session['certificate_data'] = result['certificate_data']
            request.session['last_attempt_id'] = attempt.id
            
            return redirect('study_app:quiz_results', attempt_id=attempt.id)
        else:
            return render(request, 'study_app/quiz_error.html', {
                'error': 'Failed to process quiz',
                'book': book,
                'module': module
            })
    
    return redirect('study_app:take_quiz', book_id=book_id, module_id=module_id)

@login_required
def quiz_results(request, attempt_id):
    """Display quiz results with certificate information"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    # Get certificate data from session
    certificate_data = request.session.get('certificate_data', {})
    
    context = {
        'attempt': attempt,
        'book': attempt.book,
        'module': attempt.quiz_module,
        'certificate_data': certificate_data,
        'results': attempt.evaluation_data or [],
    }
    
    # Clear session data
    if 'certificate_data' in request.session:
        del request.session['certificate_data']
    
    return render(request, 'study_app/quiz_results.html', context)

@login_required
def download_certificate(request, attempt_id):
    """Generate and download certificate PDF"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
    
    if attempt.passed:
        # Generate certificate data
        from .quiz_certificate_system import CertificateGenerator
        cert_generator = CertificateGenerator()
        
        certificate_data = cert_generator.generate_certificate_data(
            request.user, attempt.quiz_module, attempt.score, attempt.passed
        )
        
        # For now, return JSON with certificate data
        # Later we can generate actual PDF certificates
        return JsonResponse({
            'certificate_available': True,
            'certificate_data': certificate_data,
            'message': 'Certificate generation will be implemented soon'
        })
    else:
        return JsonResponse({
            'certificate_available': False,
            'message': 'Certificate requires passing score (70% or higher)'
        })
