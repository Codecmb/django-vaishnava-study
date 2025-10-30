import re

# Read the views_quiz.py file
with open('study_app/views_quiz.py', 'r') as f:
    content = f.read()

# Find and update the quiz_results function
old_results_pattern = r'def quiz_results\(request, attempt_id\):.*?return render\(request.*?\)'

new_results_function = '''def quiz_results(request, attempt_id):
    """Display quiz results with intelligent feedback"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    # Load evaluation results if available
    if attempt.evaluation_results:
        results_data = json.loads(attempt.evaluation_results)
    else:
        # Fallback: basic results from answers
        results_data = []
        answers = json.loads(attempt.answers_json) if attempt.answers_json else {}
        evaluator = AnswerEvaluator()
        
        for qid, user_answer in answers.items():
            try:
                question = QuizQuestion.objects.get(id=int(qid))
                is_correct, feedback = evaluator.evaluate_answer(int(qid), user_answer)
                
                # Get relevant commentary
                book_pdf = BookPDF.objects.filter(book=question.book).first()
                if book_pdf:
                    generator = IntelligentAnswerGenerator(book_pdf)
                    commentary = generator.find_relevant_commentary(question.question_text, question.chapter)
                else:
                    commentary = "Study the scriptures carefully."
                
                results_data.append({
                    'question_id': qid,
                    'question_text': question.question_text,
                    'user_answer': user_answer,
                    'is_correct': is_correct,
                    'feedback': feedback,
                    'commentary': commentary,
                    'guidance': "Keep studying regularly!" if is_correct else "Review this topic carefully.",
                    'score': 1 if is_correct else 0
                })
            except:
                continue
    
    context = {
        'attempt': attempt,
        'results': results_data,
    }
    return render(request, 'study_app/quiz_results.html', context)'''

# Replace the function
content = re.sub(old_results_pattern, new_results_function, content, flags=re.DOTALL)

# Write back
with open('study_app/views_quiz.py', 'w') as f:
    f.write(content)

print("Updated quiz_results function!")
