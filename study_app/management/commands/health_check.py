from django.core.management.base import BaseCommand
import time

class Command(BaseCommand):
    help = 'Fast health check'
    
    def handle(self, *args, **options):
        start = time.time()
        
        # Test core functionality with lazy imports
        from study_app.models import QuizQuestion
        from study_app.internet_answer_generator import internet_generator
        
        load_time = time.time() - start
        print(f'Module load: {load_time:.3f}s')
        
        # Quick DB test
        count = QuizQuestion.objects.count()
        print(f'Database: {count} questions found')
        
        total = time.time() - start
        status = '✓ FAST' if total < 1.0 else '⚠ SLOW'
        print(f'{status}: Total time {total:.3f}s')
