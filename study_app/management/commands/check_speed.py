from django.core.management.base import BaseCommand
import time

class Command(BaseCommand):
    help = 'Check system startup and operation speed'
    
    def handle(self, *args, **options):
        start_time = time.time()
        
        # Test basic imports
        from study_app.models import QuizQuestion, BookPDF
        from study_app.internet_answer_generator import internet_generator
        
        import_time = time.time() - start_time
        self.stdout.write(f"Import time: {import_time:.3f} seconds")
        
        # Test database query speed
        db_start = time.time()
        questions = QuizQuestion.objects.all()[:5]
        db_time = time.time() - db_start
        self.stdout.write(f"Database query time: {db_time:.3f} seconds")
        
        # Test answer generation speed
        gen_start = time.time()
        if questions:
            choices = internet_generator.generate_meaningful_choices(questions[0])
            gen_time = time.time() - gen_start
            self.stdout.write(f"Answer generation time: {gen_time:.3f} seconds")
        
        total_time = time.time() - start_time
        self.stdout.write(f"Total operation time: {total_time:.3f} seconds")
        
        if total_time < 2.0:
            self.stdout.write(self.style.SUCCESS("✓ System is running fast!"))
        else:
            self.stdout.write(self.style.WARNING("⚠ System might be slow, consider more optimizations"))
