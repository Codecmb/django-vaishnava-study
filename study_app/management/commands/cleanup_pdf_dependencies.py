from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Clean up PDF dependencies and cache to speed up the system'
    
    def handle(self, *args, **options):
        # Clear any PDF-related cache
        cache_keys = list(cache._cache.keys()) if hasattr(cache, '_cache') else []
        pdf_cache_keys = [key for key in cache_keys if 'pdf' in str(key).lower()]
        
        for key in pdf_cache_keys:
            cache.delete(key)
        
        self.stdout.write(f"Cleared {len(pdf_cache_keys)} PDF cache keys")
        
        # Update BookPDF records to disable text extraction
        try:
            from study_app.models import BookPDF
            updated = BookPDF.objects.update(text_extracted=False)
            self.stdout.write(f"Updated {updated} BookPDF records to disable text extraction")
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not update BookPDF: {e}"))
        
        self.stdout.write(self.style.SUCCESS('PDF dependencies cleaned up successfully! System should be fast now.'))
