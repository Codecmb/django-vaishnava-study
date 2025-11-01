import re

# Read the file
with open('study_app/views_quiz.py', 'r') as f:
    content = f.read()

# Find the take_quiz function and replace the POST handling part
# We need to find the section that handles form submission and replace it with intelligent evaluation

# First, let's add the necessary imports at the top if they're not there
if 'from .intelligent_answer_generator import IntelligentAnswerGenerator' not in content:
    # Add imports after the existing imports
    import_section = '''from .models import Book, QuizModule, QuizQuestion, QuizAttempt
from .forms import QuizAnswerForm
from study_app.ai_service_enhanced import get_enhanced_ai_feedback as get_ai_feedback
from .intelligent_answer_generator import IntelligentAnswerGenerator
from .answer_evaluator import AnswerEvaluator'''
    
    content = content.replace('''from .models import Book, QuizModule, QuizQuestion, QuizAttempt
from .forms import QuizAnswerForm
from study_app.ai_service_enhanced import get_enhanced_ai_feedback as get_ai_feedback''', import_section)

# Now replace the POST handling section in take_quiz
old_post_section = '''    if request.method == 'POST':
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
                score=0,  # Will be calculated
                total_questions=questions.count(),
                answers_json=json.dumps(answers)
            )
            
            # Redirect to results page
            return redirect('study_app:quiz_results', attempt_id=quiz_attempt.id)
        
        else:
            messages.error(request, 'Please correct the errors below.')'''

new_post_section = '''    if request.method == 'POST':
        form = QuizAnswerForm(request.POST, questions=questions)
        if form.is_valid():
            # Process quiz answers with intelligent evaluation
            answers = {}
            evaluator = AnswerEvaluator()
            total_score = 0
            evaluation_results = []
            
            for question in questions:
                answer_key = f'question_{question.id}'
                user_answer = form.cleaned_data.get(answer_key, '')
                answers[str(question.id)] = user_answer
                
                # Evaluate written answer intelligently
                is_correct, answer_feedback = evaluator.evaluate_answer(
                    question.id, user_answer
                )
                
                # Get relevant Prabhupada commentary
                book_pdf = BookPDF.objects.filter(book=question.book).first()
                if book_pdf:
                    generator = IntelligentAnswerGenerator(book_pdf)
                    commentary = generator.find_relevant_commentary(
                        question.question_text, question.chapter
                    )
                else:
                    commentary = "Study Bhagavad-gita As It Is carefully under proper guidance."
                
                # Generate personalized guidance
                if book_pdf:
                    guidance = generator.generate_personalized_guidance(
                        question.question_text, user_answer, is_correct
                    )
                else:
                    guidance = "Regular study and chanting will deepen spiritual realizations!"
                
                score = 1 if is_correct else 0
                total_score += score
                
                evaluation_results.append({
                    'question_id': question.id,
                    'question_text': question.question_text,
                    'user_answer': user_answer,
                    'is_correct': is_correct,
                    'feedback': answer_feedback,
                    'commentary': commentary,
                    'guidance': guidance,
                    'score': score
                })
            
            # Create quiz attempt with actual score
            quiz_attempt = QuizAttempt.objects.create(
                user=request.user if request.user.is_authenticated else None,
                book=book,
                module=module,
                score=total_score,
                total_questions=questions.count(),
                answers_json=json.dumps(answers),
                evaluation_results=json.dumps(evaluation_results)  # Store detailed results
            )
            
            # Redirect to results page
            return redirect('study_app:quiz_results', attempt_id=quiz_attempt.id)
        
        else:
            messages.error(request, 'Please correct the errors below.')'''

# Replace the section
content = content.replace(old_post_section, new_post_section)

# Also need to add BookPDF import
if 'from .models import Book, QuizModule, QuizQuestion, QuizAttempt' in content:
    content = content.replace(
        'from .models import Book, QuizModule, QuizQuestion, QuizAttempt',
        'from .models import Book, QuizModule, QuizQuestion, QuizAttempt, BookPDF'
    )

# Write the updated content back
with open('study_app/views_quiz.py', 'w') as f:
    f.write(content)

print("Updated take_quiz function with intelligent evaluation!")
