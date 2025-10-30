#!/bin/bash
echo "=== TESTING COMPLETE QUIZ SYSTEM ==="

echo "1. Testing template loading..."
python manage.py shell << EOL
from django.template.loader import get_template
try:
    template = get_template('study_app/take_quiz.html')
    print("✅ take_quiz.html template loads successfully")
    
    # Check if template has the right context
    context = {'questions': [{'id': 1, 'question_text': 'Test question', 'chapter': 'Chapter 1', 'multiple_choice_options': ''}]}
    rendered = template.render(context)
    if 'textarea' in rendered and 'question_1' in rendered:
        print("✅ Student input box renders correctly in template")
    else:
        print("❌ Student input box not rendering properly")
        
except Exception as e:
    print(f"❌ Template error: {e}")
EOL

echo ""
echo "2. Testing views..."
python manage.py shell << EOL
try:
    from study_app.views_quiz import take_quiz, quiz_results
    print("✅ Quiz views import successfully")
    
    from study_app.models import QuizQuestion, QuizAttempt
    questions = QuizQuestion.objects.count()
    attempts = QuizAttempt.objects.count()
    print(f"✅ Database has {questions} questions and {attempts} attempts")
    
except Exception as e:
    print(f"❌ Views error: {e}")
EOL

echo ""
echo "=== SYSTEM READY CHECK ==="
echo "The student input box should now be restored and working!"
