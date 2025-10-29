import os
import django
import sys

sys.path.append('/home/marlins/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from study_app.student_answer_processor import student_processor

class MockQuestion:
    def __init__(self):
        self.question_text = 'What is the eternal nature of the soul?'
        self.verse_reference = 'BG 2.13'
        self.correct_answers = ''
        self.multiple_choice_options = None

# Test the processor
question = MockQuestion()
student_answer = 'The soul cannot be destroyed'

result = student_processor.process_student_answer(question, student_answer, 'written')

print('SUCCESS! System is working:')
print('Correct Answer:', result['correct_answer'])
print('Should Save:', result['should_save'])
print('Commentary Preview:', result['prabhupada_commentary'][:100] + '...')
