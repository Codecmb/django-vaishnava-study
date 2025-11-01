#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion

print("🔧 ADDING MULTIPLE CHOICE OPTIONS TO EXISTING QUESTIONS")
print("=" * 50)

questions = QuizQuestion.objects.all()
print(f"Found {questions.count()} questions to update")

updated_count = 0
for question in questions:
    if not question.multiple_choice_options:
        # Create multiple choice options based on the question
        correct_answer = question.correct_answers.split(',')[0].strip() if question.correct_answers else "Correct Answer"
        
        # Generate wrong answers based on question content
        wrong_answers = [
            "Incorrect option 1",
            "Incorrect option 2", 
            "Incorrect option 3"
        ]
        
        # Specialize wrong answers based on question type
        if 'where' in question.question_text.lower():
            wrong_answers = ["In Vrindavan", "In Mayapur", "In Puri"]
        elif 'why' in question.question_text.lower():
            wrong_answers = ["For material gain", "For fame", "For sense gratification"]
        elif 'what' in question.question_text.lower() and 'purpose' in question.question_text.lower():
            wrong_answers = ["To become wealthy", "To enjoy senses", "To become powerful"]
        
        # Combine into pipe-separated string
        all_options = [correct_answer] + wrong_answers
        question.multiple_choice_options = '|'.join(all_options)
        question.save()
        updated_count += 1
        print(f"✅ Updated: {question.question_text[:50]}...")

print(f"\\n🎉 Updated {updated_count} questions with multiple choice options")
print(f"📊 {questions.count() - updated_count} questions already had options")

# Show sample of updated questions
print("\\n📝 SAMPLE UPDATED QUESTIONS:")
for question in QuizQuestion.objects.filter(multiple_choice_options__isnull=False)[:3]:
    options = question.get_multiple_choice_list()
    print(f"Q: {question.question_text[:60]}...")
    print(f"  Options: {options}")
    print()
