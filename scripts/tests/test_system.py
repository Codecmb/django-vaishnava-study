import os
import django
import sys

sys.path.append('/home/marlins/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.student_answer_processor import student_processor

class MockQuestion:
    def __init__(self, question_text, verse_reference):
        self.question_text = question_text
        self.verse_reference = verse_reference
        self.correct_answers = ""
        self.multiple_choice_options = None

def main():
    print("Testing Student-Driven Correct Answer System")
    print("=" * 50)
    
    question = MockQuestion(
        "What is the eternal nature of the soul?", 
        "BG 2.13"
    )
    
    student_answer = "The soul cannot be destroyed by any means"
    
    result = student_processor.process_student_answer(
        question, student_answer, "written"
    )
    
    print("SUCCESS! System is working:")
    print(f"Correct Answer: {result['correct_answer']}")
    print(f"Should Save: {result['should_save']}")
    print(f"Commentary Preview: {result['prabhupada_commentary'][:100]}...")

if __name__ == "__main__":
    main()
