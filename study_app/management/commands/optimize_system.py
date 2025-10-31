from django.core.management.base import BaseCommand
from django.db import connection
from django.core.cache import cache
import time

class Command(BaseCommand):
    help = 'Final system optimization for maximum speed'
    
    def handle(self, *args, **options):
        self.stdout.write("Optimizing system for speed...")
        
        start_time = time.time()
        
        # 1. Clear all cache
        cache.clear()
        self.stdout.write("✓ Cleared all cache")
        
        # 2. Optimize database
        with connection.cursor() as cursor:
            cursor.execute("VACUUM;")
        self.stdout.write("✓ Database optimized")
        
        # 3. Ensure no PDF text is loaded
        try:
            from study_app.models import BookPDF
            BookPDF.objects.update(extracted_text='', text_extracted=False)
            self.stdout.write("✓ All PDF text cleared")
        except Exception as e:
            self.stdout.write(f"⚠ Could not clear PDF text: {e}")
        
        # 4. Test import speed
        test_start = time.time()
        from study_app.internet_answer_generator import internet_generator
        from study_app.models import QuizQuestion
        import_time = time.time() - test_start
        self.stdout.write(f"✓ Core imports: {import_time:.3f}s")
        
        # 5. Test answer generation
        questions = QuizQuestion.objects.all()[:3]
        if questions:
            gen_start = time.time()
            for q in questions:
                internet_generator.generate_meaningful_choices(q)
            gen_time = time.time() - gen_start
            self.stdout.write(f"✓ Answer generation: {gen_time:.3f}s for 3 questions")
        
        total_time = time.time() - start_time
        self.stdout.write(self.style.SUCCESS(f"✓ Optimization complete in {total_time:.2f}s"))
        self.stdout.write("🎯 System is now optimized for speed!")
