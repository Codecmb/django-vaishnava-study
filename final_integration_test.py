import os
import django
import sys

sys.path.append('/home/marlins/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.models import QuizQuestion, QuizModule, Book
from study_app.student_answer_processor import student_processor

def test_integration():
    print("🎯 FINAL INTEGRATION TEST")
    print("=" * 50)
    
    # Get Bhakti Shastri course and its questions
    try:
        book = Book.objects.get(title='Bhagavad-gita As It Is')
        modules = QuizModule.objects.filter(course=book.course)
        
        print(f"Found {modules.count()} modules for {book.title}")
        
        for module in modules:
            questions = module.questions.all()
            print(f"Module: {module.name} - {questions.count()} questions")
            
            for question in questions:
                print(f"  Question: {question.question_text[:50]}...")
                print(f"    Current correct_answer: {question.correct_answers or 'EMPTY'}")
                
                # Test with a student answer
                if not question.correct_answers:
                    student_answer = "The soul is eternal and indestructible"
                    result = student_processor.process_student_answer(question, student_answer, 'written')
                    
                    if result['should_save']:
                        question.correct_answers = result['correct_answer']
                        question.prabhupada_commentary = result['prabhupada_commentary']
                        question.save()
                        print("    ✅ POPULATED correct_answer!")
                    else:
                        print("    ℹ️  Already has correct_answer")
                else:
                    print("    ℹ️  Already has correct_answer")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_integration()
