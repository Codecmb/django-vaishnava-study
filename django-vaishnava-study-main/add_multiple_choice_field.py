#!/usr/bin/env python3
import os
import django
import sys

sys.path.append('/home/marlins/Documents/GitHub/django-vaishnava-study')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from django.db import migrations, models

def add_multiple_choice_field(apps, schema_editor):
    QuizQuestion = apps.get_model('study_app', 'QuizQuestion')
    
    # Add field to existing questions
    for question in QuizQuestion.objects.all():
        if not hasattr(question, 'multiple_choice_options'):
            # Create basic options from correct answer
            correct = question.correct_answers
            options = f"{correct}|Wrong Answer 1|Wrong Answer 2|Wrong Answer 3"
            question.multiple_choice_options = options
            question.save()

print("This would add multiple_choice_options field to QuizQuestion")
print("But we need to create a migration first")
