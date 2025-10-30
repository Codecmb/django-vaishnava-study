"""
Updated quiz views with intelligent answer evaluation
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import QuizQuestion, QuizAttempt, Book
from .intelligent_answer_generator import IntelligentAnswerGenerator
from .answer_evaluator import AnswerEvaluator

def take_quiz(request, book_id, module_id=None):
    """Display quiz questions"""
    book = get_object_or_404(Book, id=book_id)
    
    if module_id:
        questions = QuizQuestion.objects.filter(book=book, module_id=module_id)
    else:
        questions = QuizQuestion.objects.filter(book=book)
    
    return render(request, 'study_app/take_quiz.html', {
        'book': book,
        'questions': questions,
    })

@csrf_exempt
def submit_quiz(request):
    """Evaluate quiz answers with intelligent feedback"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            book_id = data.get('book_id')
            answers = data.get('answers', {})
            
            evaluator = AnswerEvaluator()
            results = []
            total_score = 0
            
            for question_id, user_answer in answers.items():
                try:
                    question = QuizQuestion.objects.get(id=question_id)
                    
                    # Evaluate written answer
                    is_correct, answer_feedback = evaluator.evaluate_answer(
                        int(question_id), user_answer
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
                    guidance = generator.generate_personalized_guidance(
                        question.question_text, user_answer, is_correct
                    )
                    
                    # Calculate score
                    score = 1 if is_correct else 0
                    total_score += score
                    
                    results.append({
                        'question_id': question_id,
                        'question_text': question.question_text,
                        'user_answer': user_answer,
                        'is_correct': is_correct,
                        'feedback': answer_feedback,
                        'commentary': commentary,
                        'guidance': guidance,
                        'score': score,
                        'expected_answer': evaluator.get_expected_answer(int(question_id))
                    })
                    
                except Exception as e:
                    print(f"Error evaluating question {question_id}: {e}")
                    continue
            
            # Save quiz attempt
            if request.user.is_authenticated:
                quiz_attempt = QuizAttempt.objects.create(
                    user=request.user,
                    book_id=book_id,
                    score=total_score,
                    total_questions=len(answers),
                    answers_json=json.dumps(answers)
                )
            
            return JsonResponse({
                'success': True,
                'score': total_score,
                'total_questions': len(answers),
                'results': results
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
