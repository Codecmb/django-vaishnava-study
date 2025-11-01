#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import django
import sys

# Set up Django environment
sys.path.append('/home/marlins/Documents/GitHub/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, Book, Course
import time

def download_iskcon_questions():
    print("🌐 Downloading questions from ISKCON Education...")
    
    # URL of the question banks
    url = "https://iskconeducation.org/question-banks/"
    
    try:
        # Fetch the webpage
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("✅ Successfully connected to ISKCON Education")
        print(f"Page title: {soup.title.string if soup.title else 'No title'}")
        
        # Look for question bank links (this will depend on the actual page structure)
        links = soup.find_all('a', href=True)
        
        question_links = []
        for link in links:
            href = link['href']
            text = link.get_text().strip()
            # Look for Bhagavad-gita or question bank links
            if any(keyword in text.lower() for keyword in ['bhagavad', 'gita', 'question', 'bank', 'quiz']):
                question_links.append((text, href))
                print(f"Found potential question bank: {text} -> {href}")
        
        return question_links
        
    except Exception as e:
        print(f"❌ Error downloading questions: {e}")
        return []

def create_sample_questions():
    """Create sample Bhagavad-gita questions if scraping fails"""
    print("\n📝 Creating sample Bhagavad-gita questions...")
    
    # Get or create course and book
    course, created = Course.objects.get_or_create(
        name='Bhagavad-gita',
        defaults={
            'level': 'beginner', 
            'description_en': 'Bhagavad-gita As It Is study course',
            'description_es': 'Curso de estudio del Bhagavad-gita Tal Como Es'
        }
    )
    
    book, created = Book.objects.get_or_create(
        title='Bhagavad-gita As It Is',
        defaults={'course': course}
    )
    
    # Sample Bhagavad-gita questions for chapters 1-4
    sample_questions = [
        {
            'chapter': '1',
            'question_text': 'Where is the battlefield of Kurukshetra located?',
            'correct_answers': 'In modern-day Haryana, India',
            'multiple_choice_options': 'In modern-day Haryana, India|In Vrindavan|In Mayapur|In Jagannatha Puri',
            'verse_reference': 'BG 1.1'
        },
        {
            'chapter': '1', 
            'question_text': 'Why was Arjuna confused on the battlefield?',
            'correct_answers': 'He did not want to fight against his relatives and teachers',
            'multiple_choice_options': 'He did not want to fight against his relatives and teachers|He was afraid of losing|He forgot how to use his weapons|He wanted to meditate instead',
            'verse_reference': 'BG 1.28-47'
        },
        {
            'chapter': '2',
            'question_text': 'What is the first instruction Krishna gives to Arjuna in Chapter 2?',
            'correct_answers': 'Do not yield to this degrading impotence',
            'multiple_choice_options': 'Do not yield to this degrading impotence|Fight for religious principles|Surrender unto Me|Abandon all varieties of religion',
            'verse_reference': 'BG 2.2-3'
        },
        {
            'chapter': '2',
            'question_text': 'What is the nature of the soul according to Bhagavad-gita Chapter 2?',
            'correct_answers': 'The soul is eternal, indestructible, and immutable',
            'multiple_choice_options': 'The soul is eternal, indestructible, and immutable|The soul is born and dies with the body|The soul is an illusion|The soul is the mind',
            'verse_reference': 'BG 2.12-30'
        },
        {
            'chapter': '3',
            'question_text': 'What is the principle of karma-yoga?',
            'correct_answers': 'Performing one\'s prescribed duties without attachment to the results',
            'multiple_choice_options': 'Performing one\'s prescribed duties without attachment to the results|Not working at all|Working only for personal gain|Working without following any rules',
            'verse_reference': 'BG 3.1-9'
        },
        {
            'chapter': '4',
            'question_text': 'How does Krishna describe the process of transcendental knowledge?',
            'correct_answers': 'It is received through disciple succession',
            'multiple_choice_options': 'It is received through disciple succession|It comes from book study alone|It is achieved through meditation|It is inherited by birth',
            'verse_reference': 'BG 4.1-3'
        }
    ]
    
    created_count = 0
    for q_data in sample_questions:
        question, created = QuizQuestion.objects.get_or_create(
            book=book,
            chapter=q_data['chapter'],
            question_text=q_data['question_text'],
            defaults={
                'correct_answers': q_data['correct_answers'],
                'multiple_choice_options': q_data['multiple_choice_options'],
                'verse_reference': q_data['verse_reference']
            }
        )
        if created:
            created_count += 1
    
    print(f"✅ Created {created_count} sample Bhagavad-gita questions")
    return created_count

if __name__ == "__main__":
    print("🚀 ISKCON Question Bank Downloader")
    print("=" * 50)
    
    # Try to download from website
    question_links = download_iskcon_questions()
    
    if not question_links:
        print("\n⚠️  Could not find question banks automatically.")
        print("Creating sample Bhagavad-gita questions instead...")
        create_sample_questions()
    
    # Show results
    from study_app.models import QuizQuestion
    total_questions = QuizQuestion.objects.count()
    print(f"\n📊 Total questions in database: {total_questions}")
    
    if total_questions > 0:
        print("\n📖 Questions by chapter:")
        from django.db.models import Count
        chapters = QuizQuestion.objects.values('chapter').annotate(count=Count('id'))
        for chapter in chapters:
            print(f"  Chapter {chapter['chapter']}: {chapter['count']} questions")
