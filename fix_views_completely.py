import re

# Read views_quiz.py
with open('study_app/views_quiz.py', 'r') as f:
    content = f.read()

# Replace ALL instances of answers_json with answers
content = content.replace('answers_json', 'answers')

# Completely replace the quiz_results function
new_quiz_results = '''
def quiz_results(request, attempt_id):
    """Display quiz results with intelligent feedback"""
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    # Generate evaluation results from answers
    evaluation_results = []
    answers = attempt.answers if attempt.answers else {}
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
                commentary = "Study the scriptures carefully under proper guidance."
            
            # Generate guidance
            if book_pdf:
                guidance = generator.generate_personalized_guidance(
                    question.question_text, user_answer, is_correct
                )
            else:
                guidance = "Regular study and chanting will deepen spiritual realizations!"
            
            evaluation_results.append({
                'question_id': qid,
                'question_text': question.question_text,
                'user_answer': user_answer,
                'is_correct': is_correct,
                'feedback': feedback,
                'commentary': commentary,
                'guidance': guidance,
                'score': 1 if is_correct else 0
            })
        except Exception as e:
            print(f"Error evaluating question {qid}: {e}")
            # Add fallback result
            evaluation_results.append({
                'question_id': qid,
                'question_text': f"Question {qid}",
                'user_answer': user_answer,
                'is_correct': len(user_answer.strip()) > 0,
                'feedback': "Answer submitted",
                'commentary': "Focus on regular study of Bhagavad-gita",
                'guidance': "Continue your spiritual journey with determination",
                'score': 1 if len(user_answer.strip()) > 0 else 0
            })
    
    context = {
        'attempt': attempt,
        'results': evaluation_results,
    }
    return render(request, 'study_app/quiz_results.html', context)
'''

# Replace the quiz_results function
pattern = r'def quiz_results\(request, attempt_id\):.*?return render\(request.*?\)'
content = re.sub(pattern, new_quiz_results, content, flags=re.DOTALL)

# Also fix the take_quiz function to use answers instead of answers_json
old_take_quiz_creation = '''            # Create quiz attempt with actual score
            quiz_attempt = QuizAttempt.objects.create(
                user=request.user if request.user.is_authenticated else None,
                book=book,
                module=module,
                score=total_score,
                total_questions=questions.count(),
                answers_json=json.dumps(answers)
            )'''

new_take_quiz_creation = '''            # Create quiz attempt with actual score
            quiz_attempt = QuizAttempt.objects.create(
                user=request.user if request.user.is_authenticated else None,
                book=book,
                module=module,
                score=total_score,
                total_questions=questions.count(),
                answers=answers
            )'''

content = content.replace(old_take_quiz_creation, new_take_quiz_creation)

# Write back
with open('study_app/views_quiz.py', 'w') as f:
    f.write(content)

print("Fixed all field references - using 'answers' instead of 'answers_json'")
