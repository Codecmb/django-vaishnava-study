"""
Quiz Certificate System - Auto-populates answers and generates certificates
"""

from django.utils import timezone
from django.conf import settings
import os

class CertificateGenerator:
    def __init__(self):
        self.pass_threshold = 70  # 70% to pass
    
    def generate_certificate_data(self, user, module, score, passed):
        """Generate certificate data for a completed module"""
        certificate_data = {
            'student_name': user.get_full_name() or user.username,
            'course_name': module.course.name,
            'module_name': module.name,
            'completion_date': timezone.now().strftime('%B %d, %Y'),
            'score': f"{score:.1f}%",
            'passed': passed,
            'certificate_id': f"BSC-{module.id:04d}-{user.id:05d}-{int(timezone.now().timestamp())}",
        }
        
        if passed:
            certificate_data['status'] = 'Successfully Completed'
            certificate_data['message'] = f'Has successfully completed {module.name} with a score of {score:.1f}%'
        else:
            certificate_data['status'] = 'Attempt Recorded'
            certificate_data['message'] = f'Has attempted {module.name} with a score of {score:.1f}%'
        
        return certificate_data
    
    def should_issue_certificate(self, score):
        """Determine if certificate should be issued based on score"""
        return score >= self.pass_threshold

class QuizCompletionSystem:
    def __init__(self):
        self.certificate_generator = CertificateGenerator()
        self.pass_threshold = 70
    
    def process_quiz_completion(self, attempt, student_answers):
        """
        Process complete quiz attempt, populate answers, and generate certificate
        """
        from .student_answer_processor import student_processor
        
        questions = attempt.quiz_module.questions.all()
        results = []
        total_score = 0
        populated_answers = 0
        
        # Process each question
        for question in questions:
            answer_key = str(question.id)
            if answer_key not in student_answers:
                continue
                
            student_answer_data = student_answers[answer_key]
            student_answer = student_answer_data.get('answer', '')
            answer_type = student_answer_data.get('type', 'written')
            
            # Process answer and get correct answer to store
            processing_result = student_processor.process_student_answer(
                question, student_answer, answer_type
            )
            
            # Update question with correct answer and commentary if not already set
            if processing_result['should_save']:
                question.correct_answers = processing_result['correct_answer']
                question.prabhupada_commentary = processing_result['prabhupada_commentary']
                question.save()
                populated_answers += 1
            
            # Evaluate correctness
            is_correct = self.evaluate_correctness(
                student_answer, 
                processing_result['correct_answer'], 
                answer_type
            )
            score = 100 if is_correct else 0
            
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
        passed = overall_score >= self.pass_threshold
        
        # Update attempt
        attempt.score = overall_score
        attempt.answers_data = student_answers
        attempt.evaluation_data = results
        attempt.completed_at = timezone.now()
        attempt.passed = passed
        attempt.save()
        
        # Generate certificate data
        certificate_data = self.certificate_generator.generate_certificate_data(
            attempt.user, attempt.quiz_module, overall_score, passed
        )
        
        return {
            'success': True,
            'overall_score': overall_score,
            'passed': passed,
            'results': results,
            'populated_answers': populated_answers,
            'certificate_data': certificate_data,
            'attempt_id': attempt.id
        }
    
    def evaluate_correctness(self, student_answer, correct_answer, answer_type):
        """Evaluate if student answer is correct"""
        if answer_type == 'multiple_choice':
            return student_answer.lower() == correct_answer.lower()
        else:
            # For written answers, check key concept matches
            student_lower = student_answer.lower()
            correct_lower = correct_answer.lower()
            
            # Extract meaningful words (longer than 3 characters)
            key_words = [word for word in correct_lower.split() if len(word) > 3]
            if not key_words:
                return False
                
            matches = sum(1 for word in key_words if word in student_lower)
            match_percentage = (matches / len(key_words)) * 100
            
            return match_percentage >= 50  # 50% match for written answers

# Global instance
quiz_system = QuizCompletionSystem()
