#!/usr/bin/env python3
import os
import django
import sys

# Set up Django environment
sys.path.append('/home/marlins/Documents/GitHub/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, Book, Course, QuizModule

def load_bhagavad_gita_questions():
    print("📖 Loading Bhagavad-gita Questions for Chapters 1-4...")
    
    # Get or create course and book
    course, created = Course.objects.get_or_create(
        name='Bhagavad-gita',
        defaults={
            'level': 'beginner', 
            'description_en': 'Bhagavad-gita As It Is study course',
            'order': 1
        }
    )
    print(f"Course: {course.name}")
    
    book, created = Book.objects.get_or_create(
        title='Bhagavad-gita As It Is',
        defaults={'course': course, 'order': 1}
    )
    print(f"Book: {book.title}")
    
    # Create a quiz module (required field)
    module, created = QuizModule.objects.get_or_create(
        name='Bhagavad-gita Chapters 1-4',
        course=course,
        defaults={
            'description': 'Questions from Bhagavad-gita Chapters 1 to 4',
            'chapters_range': '1-4',
            'order': 1
        }
    )
    print(f"Module: {module.name}")
    
    # Bhagavad-gita Chapter 1 Questions
    chapter1_questions = [
        {
            'question': 'Where is the battlefield of Kurukshetra located?',
            'correct': 'In modern-day Haryana, India',
            'options': 'In modern-day Haryana, India|In Vrindavan|In Mayapur|In Jagannatha Puri',
            'verse': 'BG 1.1'
        },
        {
            'question': 'Why was Arjuna confused on the battlefield?',
            'correct': 'He did not want to fight against his relatives and teachers',
            'options': 'He did not want to fight against his relatives and teachers|He was afraid of losing|He forgot how to use his weapons|He wanted to meditate instead',
            'verse': 'BG 1.28-47'
        }
    ]
    
    # Bhagavad-gita Chapter 2 Questions
    chapter2_questions = [
        {
            'question': 'What is the first instruction Krishna gives to Arjuna in Chapter 2?',
            'correct': 'Do not yield to this degrading impotence',
            'options': 'Do not yield to this degrading impotence|Fight for religious principles|Surrender unto Me|Abandon all varieties of religion',
            'verse': 'BG 2.2-3'
        },
        {
            'question': 'What is the nature of the soul according to Bhagavad-gita Chapter 2?',
            'correct': 'The soul is eternal, indestructible, and immutable',
            'options': 'The soul is eternal, indestructible, and immutable|The soul is born and dies with the body|The soul is an illusion|The soul is the mind',
            'verse': 'BG 2.12-30'
        }
    ]
    
    # Load questions into database
    created_count = 0
    
    # Chapter 1 questions
    for i, q_data in enumerate(chapter1_questions):
        question, created = QuizQuestion.objects.get_or_create(
            book=book,
            module=module,
            chapter='1',
            question_text=q_data['question'],
            defaults={
                'correct_answers': q_data['correct'],
                'multiple_choice_options': q_data['options'],
                'verse_reference': q_data['verse'],
                'order': i + 1
            }
        )
        if created:
            created_count += 1
    
    # Chapter 2 questions  
    for i, q_data in enumerate(chapter2_questions):
        question, created = QuizQuestion.objects.get_or_create(
            book=book,
            module=module,
            chapter='2',
            question_text=q_data['question'],
            defaults={
                'correct_answers': q_data['correct'],
                'multiple_choice_options': q_data['options'],
                'verse_reference': q_data['verse'],
                'order': i + len(chapter1_questions) + 1
            }
        )
        if created:
            created_count += 1
    
    print(f"✅ Successfully loaded {created_count} Bhagavad-gita questions!")
    return created_count

if __name__ == "__main__":
    load_bhagavad_gita_questions()
    
    # Show results
    from study_app.models import QuizQuestion
    total = QuizQuestion.objects.count()
    print(f"\n📊 Total questions in database: {total}")
    
    if total > 0:
        from django.db.models import Count
        chapters = QuizQuestion.objects.values('chapter').annotate(count=Count('id'))
        print("\n📖 Questions by chapter:")
        for chapter in chapters:
            print(f"  Chapter {chapter['chapter']}: {chapter['count']} questions")
        
        print("\n🔍 Sample questions:")
        for q in QuizQuestion.objects.all()[:3]:
            print(f"  - Chapter {q.chapter}: {q.question_text}")
