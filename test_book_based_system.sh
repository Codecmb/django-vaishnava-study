#!/bin/bash
echo "=== Testing Book-Based Quiz Evaluation ==="

echo "1. Testing PDF commentary service..."
python manage.py shell << EOL
from study_app.pdf_commentary_service import pdf_commentary
print("Loaded PDF books:", list(pdf_commentary.pdf_content.keys()))

# Test commentary extraction
question = "What is the nature of the soul according to Bhagavad-gita?"
answer = "The soul is eternal, indestructible, and full of knowledge"
commentary = pdf_commentary.find_relevant_commentary(question, answer)
print("Commentary sample:", commentary[:200] + "..." if len(commentary) > 200 else commentary)
EOL

echo "2. Testing book-based evaluator..."
python manage.py shell << EOL
from study_app.book_based_evaluator import book_evaluator

test_cases = [
    ("What is bhakti yoga?", "Bhakti yoga is the process of devotional service to Krishna"),
    ("Who is Arjuna?", "Arjuna is the friend and devotee of Krishna in Bhagavad-gita"),
    ("What is karma?", "Karma refers to material activities and their reactions")
]

for i, (question, answer) in enumerate(test_cases):
    is_correct, feedback, commentary = book_evaluator.evaluate_answer(question, answer)
    print(f"Test {i+1}: {question}")
    print(f"  Correct: {is_correct}")
    print(f"  Feedback: {feedback}")
    print(f"  Commentary length: {len(commentary)} characters")
    print()
EOL

echo "3. Testing quiz models..."
python manage.py shell << EOL
from study_app.models import QuizAttempt, QuizQuestion
attempts = QuizAttempt.objects.all()
print(f"Found {attempts.count()} quiz attempts")

for attempt in attempts[:2]:  # Test first 2 attempts
    print(f"Attempt {attempt.id}: {attempt.book.title}")
    score = attempt.calculate_score()
    print(f"  Score: {score}/{len(attempt.answers)}")
EOL

echo "=== Book-Based Evaluation Test Complete ==="
