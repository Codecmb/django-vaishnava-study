#!/usr/bin/env python3
import os
import django
import sys

# Setup Django environment
sys.path.append('/home/marlins/Documents/GitHub/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, Book, Course, QuizModule

def create_bhagavad_gita_questions():
    """
    Independently create Bhagavad-gita questions for each chapter
    This script doesn't modify existing data - only adds new questions
    """
    print("🚀 Creating Bhagavad-gita Questions Independently")
    print("=" * 50)
    
    # Get or create course (won't affect existing ones)
    course, course_created = Course.objects.get_or_create(
        name='Bhagavad-gita',
        defaults={
            'level': 'beginner', 
            'description_en': 'Bhagavad-gita As It Is study course',
            'order': 1
        }
    )
    if course_created:
        print(f"✅ Created new course: {course.name}")
    else:
        print(f"📚 Using existing course: {course.name}")
    
    # Get or create book
    book, book_created = Book.objects.get_or_create(
        title='Bhagavad-gita As It Is',
        defaults={'course': course, 'order': 1}
    )
    if book_created:
        print(f"✅ Created new book: {book.title}")
    else:
        print(f"📖 Using existing book: {book.title}")
    
    # Create questions for each chapter independently
    chapters_questions = {
        '1': [
            {
                'question': 'Where is the battlefield of Kurukshetra located?',
                'correct': 'In modern-day Haryana, India',
                'options': 'In modern-day Haryana, India|In Vrindavan|In Mayapur|In Jagannatha Puri',
                'verse': 'BG 1.1',
                'commentary': 'Kurukshetra is a holy place of pilgrimage...'
            },
            {
                'question': 'Why was Arjuna confused on the battlefield of Kurukshetra?',
                'correct': 'He did not want to fight against his relatives and teachers',
                'options': 'He did not want to fight against his relatives and teachers|He was afraid of losing the battle|He forgot how to use his weapons|He wanted to meditate instead of fighting',
                'verse': 'BG 1.28-47',
                'commentary': 'Arjuna was a great devotee of the Lord, but he was affected by temporary illusion...'
            }
        ],
        '2': [
            {
                'question': 'What is the first instruction Krishna gives to Arjuna in Chapter 2?',
                'correct': 'Do not yield to this degrading impotence',
                'options': 'Do not yield to this degrading impotence|Fight for religious principles|Surrender unto Me|Abandon all varieties of religion',
                'verse': 'BG 2.2-3',
                'commentary': 'The Lord does not approve of the so-called compassion of Arjuna for his kinsmen...'
            },
            {
                'question': 'What is the nature of the soul according to Bhagavad-gita Chapter 2?',
                'correct': 'The soul is eternal, indestructible, and immutable',
                'options': 'The soul is eternal, indestructible, and immutable|The soul is born and dies with the body|The soul is an illusion|The soul is the mind',
                'verse': 'BG 2.12-30',
                'commentary': 'The soul is eternal and cannot be destroyed by any means...'
            }
        ],
        '3': [
            {
                'question': 'What is the principle of karma-yoga according to Chapter 3?',
                'correct': 'Performing ones prescribed duties without attachment to the results',
                'options': 'Performing ones prescribed duties without attachment to the results|Not working at all|Working only for personal gain|Working without following any rules',
                'verse': 'BG 3.1-9',
                'commentary': 'Work done as a sacrifice for Vishnu has to be performed...'
            }
        ],
        '4': [
            {
                'question': 'How does Krishna describe the process of transcendental knowledge?',
                'correct': 'It is received through disciple succession',
                'options': 'It is received through disciple succession|It comes from book study alone|It is achieved through meditation|It is inherited by birth',
                'verse': 'BG 4.1-3',
                'commentary': 'The sun-god Vivasvan taught this science to his son...'
            }
        ]
    }
    
    # Create module for each chapter independently
    total_created = 0
    for chapter_num, questions in chapters_questions.items():
        # Create separate module for each chapter
        module, module_created = QuizModule.objects.get_or_create(
            name=f'Bhagavad-gita Chapter {chapter_num}',
            course=course,
            defaults={
                'description': f'Questions from Bhagavad-gita Chapter {chapter_num}',
                'chapters_range': chapter_num,
                'order': int(chapter_num)
            }
        )
        
        if module_created:
            print(f"✅ Created new module: {module.name}")
        else:
            print(f"📂 Using existing module: {module.name}")
        
        # Add questions for this chapter
        chapter_created = 0
        for i, q_data in enumerate(questions):
            question, created = QuizQuestion.objects.get_or_create(
                book=book,
                module=module,
                chapter=chapter_num,
                question_text=q_data['question'],
                defaults={
                    'correct_answers': q_data['correct'],
                    'multiple_choice_options': q_data['options'],
                    'verse_reference': q_data['verse'],
                    'prabhupada_commentary': q_data.get('commentary', ''),
                    'order': i + 1
                }
            )
            if created:
                chapter_created += 1
                total_created += 1
        
        print(f"   ➕ Added {chapter_created} questions for Chapter {chapter_num}")
    
    print(f"\n🎉 SUCCESS: Created {total_created} new questions across {len(chapters_questions)} chapters")
    
    # Show final summary without affecting data
    from django.db.models import Count
    total_questions = QuizQuestion.objects.count()
    chapters_summary = QuizQuestion.objects.values('chapter').annotate(count=Count('id')).order_by('chapter')
    
    print(f"\n📊 DATABASE SUMMARY:")
    print(f"   Total questions: {total_questions}")
    print(f"   Questions by chapter:")
    for chapter in chapters_summary:
        print(f"     Chapter {chapter['chapter']}: {chapter['count']} questions")

def check_current_data():
    """Safe function to check current data without modifications"""
    print("\n🔍 CURRENT DATA CHECK:")
    print("=" * 30)
    
    from study_app.models import QuizQuestion, Course, Book, QuizModule
    
    print(f"Courses: {Course.objects.count()}")
    print(f"Books: {Book.objects.count()}")
    print(f"Modules: {QuizModule.objects.count()}")
    print(f"Questions: {QuizQuestion.objects.count()}")
    
    if QuizQuestion.objects.count() > 0:
        from django.db.models import Count
        chapters = QuizQuestion.objects.values('chapter').annotate(count=Count('id')).order_by('chapter')
        print("\nCurrent questions by chapter:")
        for chapter in chapters:
            print(f"  Chapter {chapter['chapter']}: {chapter['count']} questions")

if __name__ == "__main__":
    # First, show current state
    check_current_data()
    
    print("\n" + "=" * 50)
    
    # Ask for confirmation before making changes
    response = input("\nDo you want to create Bhagavad-gita questions? (y/N): ")
    if response.lower() in ['y', 'yes']:
        create_bhagavad_gita_questions()
    else:
        print("No changes made. Exiting safely.")
    
    print("\n" + "=" * 50)
    print("Script completed safely. No existing data was modified.")

