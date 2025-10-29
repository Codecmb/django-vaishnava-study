#!/usr/bin/env python3
import os
import django
import sys
import json

sys.path.append('/home/marlins/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, QuizModule, Book

def create_chapter_questions():
    """Create professional multiple-choice questions for all Bhagavad-gita chapters"""
    
    bg_book = Book.objects.filter(title='Bhagavad-gita As It Is').first()
    if not bg_book:
        print("Bhagavad-gita book not found")
        return
    
    # Questions for each chapter
    chapter_questions = {
        1: [
            {
                'question': 'Why was Duryodhana confident of support from Bhismadeva and Dronacarya?',
                'verse': 'BG 1.11',
                'options': [
                    "They were bound by duty as military commanders",
                    "Duryodhana paid them money",
                    "They disliked the Pandavas", 
                    "Krishna instructed them"
                ],
                'correct_answer': "They were bound by duty as military commanders",
                'guidance': "Military commanders were bound by duty, not personal preference."
            },
            {
                'question': 'What is the meaning of gudakesa?',
                'verse': 'BG 1.24',
                'options': [
                    "One who conquered sleep",
                    "Master of senses", 
                    "Lord of earth",
                    "Conqueror of enemies"
                ],
                'correct_answer': "One who conquered sleep",
                'guidance': "Refers to controlling bodily demands like sleep."
            }
        ],
        2: [
            {
                'question': 'What is the eternal nature of the soul according to BG 2.13?',
                'verse': 'BG 2.13',
                'options': [
                    "The soul is eternal and indestructible",
                    "The soul dies with the body",
                    "The soul is temporary", 
                    "The soul doesnt exist"
                ],
                'correct_answer': "The soul is eternal and indestructible",
                'guidance': "The soul cannot be killed, burned, wet, or dried."
            },
            {
                'question': 'How does the soul transmigrate according to BG 2.22?',
                'verse': 'BG 2.22', 
                'options': [
                    "Like changing clothes",
                    "Through rebirth as animals only",
                    "It doesnt transmigrate",
                    "Through mental speculation"
                ],
                'correct_answer': "Like changing clothes",
                'guidance': "The soul changes bodies just as a person changes garments."
            }
        ],
        3: [
            {
                'question': 'What is the duty of a wise person according to BG 3.8?',
                'verse': 'BG 3.8',
                'options': [
                    "Perform prescribed duties",
                    "Renounce all action", 
                    "Act for sense gratification",
                    "Avoid all responsibilities"
                ],
                'correct_answer': "Perform prescribed duties",
                'guidance': "One should perform prescribed duties without attachment."
            }
        ],
        4: [
            {
                'question': 'How does Krishna descend according to BG 4.7?',
                'verse': 'BG 4.7',
                'options': [
                    "To protect devotees and annihilate miscreants",
                    "For sense enjoyment", 
                    "By chance or accident",
                    "Only in Kali-yuga"
                ],
                'correct_answer': "To protect devotees and annihilate miscreants",
                'guidance': "Krishna descends to establish dharma and protect devotees."
            }
        ]
        # Add more chapters as needed...
    }
    
    total_created = 0
    for chapter_num, questions in chapter_questions.items():
        module_name = f'Bhagavad-gita Chapter {chapter_num}'
        module = QuizModule.objects.filter(name=module_name).first()
        
        if not module:
            print(f"❌ Module not found: {module_name}")
            continue
            
        # Clear existing questions for this module (optional)
        # module.questions.all().delete()
        
        chapter_created = 0
        for i, q_data in enumerate(questions, 1):
            if not QuizQuestion.objects.filter(question_text=q_data['question']).exists():
                QuizQuestion.objects.create(
                    book=bg_book,
                    module=module,
                    chapter=f'Chapter {chapter_num}',
                    question_text=q_data['question'],
                    correct_answers=q_data['correct_answer'],
                    verse_reference=q_data['verse'],
                    additional_guidance=q_data['guidance'],
                    multiple_choice_options=json.dumps(q_data['options']),
                    order=i * 10
                )
                chapter_created += 1
        
        total_created += chapter_created
        print(f"✅ Chapter {chapter_num}: Created {chapter_created} questions")
    
    print(f"\n🎉 TOTAL: Created {total_created} professional questions across {len(chapter_questions)} chapters")
    
    # Show summary
    modules = QuizModule.objects.filter(name__startswith='Bhagavad-gita Chapter')
    print(f"\n📊 SUMMARY - Questions per chapter:")
    for module in modules.order_by('order'):
        count = module.questions.count()
        print(f"  {module.name}: {count} questions")

if __name__ == "__main__":
    create_chapter_questions()
