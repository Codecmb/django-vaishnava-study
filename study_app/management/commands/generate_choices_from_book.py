from django.core.management.base import BaseCommand
from study_app.models import QuizQuestion
from study_app.pure_pdf_answer_generator import pure_pdf_generator
import json

class Command(BaseCommand):
    help = 'Generate multiple choice options using ONLY the actual book content'
    
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
        parser.add_argument(
            '--replace-existing',
            action='store_true',
            help='Replace existing choices with book-based ones'
        )
    
    def handle(self, *args, **options):
        if options['question_id']:
            questions = QuizQuestion.objects.filter(id=options['question_id'])
        elif options['all']:
            if options['replace_existing']:
                questions = QuizQuestion.objects.all()
            else:
                questions = QuizQuestion.objects.filter(multiple_choice_options__isnull=True)
        else:
            questions = QuizQuestion.objects.filter(multiple_choice_options__isnull=True)
        
        updated_count = 0
        
        for question in questions:
            if self.generate_book_based_choices(question):
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated book-based choices for {updated_count} questions')
        )
    
    def generate_book_based_choices(self, question):
        """Generate choices using ONLY the book content"""
        try:
            # Use pure book-based generator
            book_choices = pure_pdf_generator.generate_choices_from_book_only(question)
            
            # Save as JSON
            question.multiple_choice_options = json.dumps(book_choices)
            question.save()
            
            self.stdout.write(f'Book-based choices for: {question.question_text[:50]}...')
            self.stdout.write(f'  Options: {book_choices}')
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error for question {question.id}: {e}'))
            return False
