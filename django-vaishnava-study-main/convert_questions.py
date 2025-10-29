#!/usr/bin/env python3
import os
import django
import sys
import json

sys.path.append('/home/marlins/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, QuizModule

def convert_to_professional_format():
    """Convert existing questions to professional multiple-choice format"""
    
    # Get Bhagavad-gita Chapter 1 module
    module = QuizModule.objects.filter(name='Bhagavad-gita Chapter 1').first()
    if not module:
        print("Bhagavad-gita Chapter 1 module not found")
        return
    
    # Sample professional questions for Chapter 1
    professional_questions = [
        {
            'question': 'Why was Duryodhana confident of full support from Bhismadeva and Dronacarya?',
            'verse': 'BG 1.11',
            'options': [
                "Because they were bound by their duty as military commanders",
                "Because Duryodhana had paid them large sums of money",
                "Because they personally disliked the Pandavas",
                "Because Krishna had instructed them to support Duryodhana"
            ],
            'correct_answer': "Because they were bound by their duty as military commanders",
            'guidance': "Consider the principles of military duty and loyalty that bound these commanders."
        },
        {
            'question': 'What is the meaning of the word gudakesa?',
            'verse': 'BG 1.24',
            'options': [
                "One who has conquered sleep",
                "Master of the senses",
                "Lord of the earth",
                "Conqueror of enemies"
            ],
            'correct_answer': "One who has conquered sleep",
            'guidance': "This name refers to Arjuna's ability to control bodily demands like sleep."
        },
        {
            'question': 'Which quality of Arjuna makes him fit to receive the knowledge of Bhagavad-gita?',
            'verse': 'BG 1.1-46',
            'options': [
                "His complete surrender to Krishna as the spiritual master",
                "His great military prowess and skills",
                "His high birth in the royal family",
                "His extensive knowledge of scriptures"
            ],
            'correct_answer': "His complete surrender to Krishna as the spiritual master",
            'guidance': "The key qualification is surrender to the spiritual master, not material qualifications."
        },
        {
            'question': 'What is the significance of Dhrtarastra usage of the word mamakah?',
            'verse': 'BG 1.1',
            'options': [
                "It reveals his attachment and sense of false proprietorship",
                "It shows his great love for his sons",
                "It indicates his royal authority",
                "It demonstrates his humility"
            ],
            'correct_answer': "It reveals his attachment and sense of false proprietorship",
            'guidance': "The word 'mamakah' means 'my men' and shows material attachment."
        },
        {
            'question': 'According to Srila Prabhupada, where does ones real self-interest lie?',
            'verse': 'BG 1.30',
            'options': [
                "In Vishnu, or Krishna",
                "In family protection and welfare",
                "In religious principles alone",
                "In economic development"
            ],
            'correct_answer': "In Vishnu, or Krishna",
            'guidance': "Real self-interest is spiritual, not material - it lies in our relationship with Krishna."
        }
    ]
    
    created_count = 0
    for i, q_data in enumerate(professional_questions, 1):
        # Check if question already exists
        if not QuizQuestion.objects.filter(question_text=q_data['question']).exists():
            question = QuizQuestion.objects.create(
                book=module.course.book_set.first(),
                module=module,
                chapter='Chapter 1',
                question_text=q_data['question'],
                correct_answers=q_data['correct_answer'],
                verse_reference=q_data['verse'],
                additional_guidance=q_data['guidance'],
                multiple_choice_options=json.dumps(q_data['options']),
                order=i * 10
            )
            created_count += 1
            print(f"✅ Created: {q_data['question'][:50]}...")
    
    print(f"🎉 Created {created_count} professional format questions for Chapter 1")
    
    # Show the new structure
    questions = module.questions.all()
    print(f"\n📊 Module now has {questions.count()} questions")
    for q in questions:
        print(f"  - {q.question_text[:60]}...")

if __name__ == "__main__":
    convert_to_professional_format()
