"""
Fixed Quiz Evaluation - Populates correct_answers after student input
"""

from django.utils import timezone
from .student_answer_processor import student_processor
from .models import QuizAttempt, QuizQuestion

def evaluate_and_store_answers(attempt, student_answers):
    """
    Evaluate quiz and populate correct_answers fields
    """
    questions = attempt.quiz_module.questions.all()
    results = []
    total_score = 0
    updated_questions = 0
    
    for question in questions:
        answer_key = str(question.id)
        if answer_key not in student_answers:
            continue
            
        student_answer_data = student_answers[answer_key]
        student_answer = student_answer_data.get('answer', '')
        answer_type = student_answer_data.get('type', 'written')
        
        # Process student answer and get correct answer to store
        processing_result = student_processor.process_student_answer(
            question, student_answer, answer_type
        )
        
        # Update the question with correct answer and commentary if needed
        if processing_result['should_save']:
            question.correct_answers = processing_result['correct_answer']
            question.prabhupada_commentary = processing_result['prabhupada_commentary']
            question.save()
            updated_questions += 1
        
        # Evaluate if student answer is correct
        is_correct = self.evaluate_correctness(student_answer, processing_result['correct_answer'], answer_type)
        score = 100 if is_correct else 0
        
        # Store result for display
        results.append({
            'question_id': question.id,
            'question_text': question.question_text,
            'student_answer': student_answer,
            'correct_answer': processing_result['correct_answer'],
            'prabhupada_commentary': processing_result['prabhupada_commentary'],
            'is_correct': is_correct,
            'score': score,
            'verse_reference': question.verse_reference,
            'answer_type': answer_type
        })
        
        total_score += score
    
    # Calculate overall score
    overall_score = total_score / len(questions) if questions else 0
    
    # Update attempt
    attempt.score = overall_score
    attempt.answers_data = student_answers
    attempt.evaluation_data = results
    attempt.completed_at = timezone.now()
    attempt.save()
    
    return {
        'success': True,
        'overall_score': overall_score,
        'results': results,
        'updated_questions': updated_questions,
        'attempt_id': attempt.id
    }

def evaluate_correctness(student_answer, correct_answer, answer_type):
    """Simple evaluation of correctness"""
    if answer_type == 'multiple_choice':
        return student_answer.lower() == correct_answer.lower()
    else:
        # For written answers, check if key concepts are present
        student_lower = student_answer.lower()
        correct_lower = correct_answer.lower()
        
        # Extract key words from correct answer (words longer than 4 characters)
        key_words = [word for word in correct_lower.split() if len(word) > 4]
        matches = sum(1 for word in key_words if word in student_lower)
        
        return matches >= len(key_words) * 0.5  # 50% match threshold
