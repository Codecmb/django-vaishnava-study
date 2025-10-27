from django.core.management.base import BaseCommand
from study_app.models import QuizQuestion
import json
import random

class Command(BaseCommand):
    help = 'Generate multiple choice options for quiz questions'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--question-id',
            type=int,
            help='Generate choices for a specific question ID'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Generate choices for all questions'
        )
    
    def handle(self, *args, **options):
        if options['question_id']:
            questions = QuizQuestion.objects.filter(id=options['question_id'])
        elif options['all']:
            questions = QuizQuestion.objects.all()
        else:
            questions = QuizQuestion.objects.filter(multiple_choice_options__isnull=True)
        
        updated_count = 0
        
        for question in questions:
            if not self.generate_choices_for_question(question):
                continue
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated choices for {updated_count} questions')
        )
    
    def generate_choices_for_question(self, question):
        """Generate multiple choice options for a question"""
        question_text = question.question_text.lower()
        
        # Define answer templates based on question content
        if 'who is krsna' in question_text:
            correct_answer = "The Supreme Personality of Godhead"
            distractors = [
                "A historical figure from India",
                "A mythological character from ancient texts",
                "A great philosopher and teacher",
                "A symbol of cosmic energy"
            ]
        elif 'relationship with krsna' in question_text:
            correct_answer = "We are eternal servants of Krsna"
            distractors = [
                "Krsna is our distant ancestor",
                "We are independent of Krsna",
                "Krsna is a imaginary concept",
                "We are equal to Krsna in all aspects"
            ]
        elif 'aim of krsna consciousness' in question_text or 'purpose' in question_text:
            correct_answer = "To develop pure love for Godhead"
            distractors = [
                "To achieve material success",
                "To gain mystical powers",
                "To escape all responsibilities",
                "To become famous and respected"
            ]
        elif 'religion' in question_text and 'faith' in question_text:
            correct_answer = "Religion is eternal, faith can change"
            distractors = [
                "Religion changes, faith is eternal",
                "Both religion and faith change frequently",
                "Neither religion nor faith can ever change",
                "Religion is man-made, faith is divine"
            ]
        else:
            # Generic philosophical questions
            correct_answer = "Based on the teachings of Srila Prabhupada"
            distractors = [
                "According to modern scientific theories",
                "Based on personal speculation",
                "As per popular cultural beliefs",
                "According to political ideologies"
            ]
        
        # Create choices list with correct answer and distractors
        choices = [correct_answer] + random.sample(distractors, 3)
        random.shuffle(choices)  # Shuffle so correct answer isn't always first
        
        # Save as JSON
        question.multiple_choice_options = json.dumps(choices)
        question.save()
        
        self.stdout.write(f'Generated choices for: {question.question_text[:50]}...')
        return True
