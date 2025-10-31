from django.core.management.base import BaseCommand
import json
import random

class Command(BaseCommand):
    help = 'Generate high-quality multiple choice options - optimized version'
    
    def add_arguments(self, parser):
        parser.add_argument('--all', action='store_true', help='Generate choices for all questions')
        parser.add_argument('--fast', action='store_true', help='Fast mode')
    
    def handle(self, *args, **options):
        # Lazy import to speed up command discovery
        from study_app.models import QuizQuestion
        from study_app.internet_answer_generator import internet_generator
        
        if options['all']:
            questions = QuizQuestion.objects.all()
        else:
            questions = QuizQuestion.objects.filter(multiple_choice_options__isnull=True)
        
        updated_count = 0
        
        for question in questions:
            try:
                choices = internet_generator.generate_meaningful_choices(question)
                question.multiple_choice_options = json.dumps(choices)
                
                if not question.prabhupada_commentary:
                    question.prabhupada_commentary = internet_generator.generate_commentary(question)
                
                question.save()
                updated_count += 1
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'Enhanced {updated_count} questions'))
