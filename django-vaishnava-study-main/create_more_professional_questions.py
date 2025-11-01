#!/usr/bin/env python3
import os
import django
import sys
import json

sys.path.append('/home/marlins/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, QuizModule, Book

def create_comprehensive_questions():
    """Create comprehensive professional questions for Chapter 1"""
    
    bg_book = Book.objects.filter(title='Bhagavad-gita As It Is').first()
    module = QuizModule.objects.filter(name='Bhagavad-gita Chapter 1').first()
    
    if not bg_book or not module:
        print("Book or module not found")
        return
    
    # Comprehensive professional questions for Chapter 1
    questions = [
        {
            'question': 'Why was Duryodhana confident of full support from Bhismadeva and Dronacarya?',
            'verse': 'BG 1.11',
            'options': [
                "They were bound by their duty as military commanders",
                "Duryodhana had paid them large sums of money",
                "They personally disliked the Pandavas",
                "Krishna had instructed them to support Duryodhana"
            ],
            'correct_answer': "They were bound by their duty as military commanders",
            'guidance': "Military commanders were bound by duty to serve the ruler, regardless of personal feelings."
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
            'guidance': "Gudakesa refers to one who has control over bodily demands like sleep."
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
            'guidance': "Mamakah means 'my men' showing material attachment and false proprietorship."
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
            'guidance': "Real self-interest is spiritual, centered on our relationship with Krishna."
        },
        {
            'question': 'What was the significance of the battlefield being called dharma-ksetre?',
            'verse': 'BG 1.1',
            'options': [
                "It was a holy place where religious principles would be established",
                "It was named after King Dharma",
                "It was a testing ground for weapons",
                "It was where economic policies were made"
            ],
            'correct_answer': "It was a holy place where religious principles would be established",
            'guidance': "Dharma-ksetre means 'the place of religious principles' indicating the spiritual significance."
        },
        {
            'question': 'Why did Arjuna request Krishna to place the chariot between the two armies?',
            'verse': 'BG 1.21-22',
            'options': [
                "To see who was present and who he had to fight",
                "To show his chariot to the opponents",
                "To retreat from the battlefield",
                "To deliver a speech to both armies"
            ],
            'correct_answer': "To see who was present and who he had to fight",
            'guidance': "Arjuna wanted to see who he was about to engage in battle with."
        }
    ]
    
    created_count = 0
    for i, q_data in enumerate(questions, 1):
        if not QuizQuestion.objects.filter(question_text=q_data['question']).exists():
            QuizQuestion.objects.create(
                book=bg_book,
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
            print(f"✅ Created: {q_data['question']}")
    
    print(f"🎉 Created {created_count} professional questions for Chapter 1")
    
    # Show final count
    final_count = module.questions.count()
    print(f"📊 Chapter 1 now has {final_count} professional multiple-choice questions")

if __name__ == "__main__":
    create_comprehensive_questions()
