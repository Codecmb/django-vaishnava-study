from django.core.management.base import BaseCommand
from study_app.book_services.pdf_extractor import BookExtractor

class Command(BaseCommand):
    help = 'Extract books - smart detection or force all'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force extract all books (ignore already extracted)',
        )
        parser.add_argument(
            '--book',
            type=str,
            help='Extract specific book by filename',
        )
    
    def handle(self, *args, **options):
        extractor = BookExtractor()
        
        if options['book']:
            self.stdout.write(f"📖 Extracting specific book: {options['book']}")
            result = extractor.extract_specific_book(options['book'])
            if result:
                self._print_result(result)
            else:
                self.stdout.write(self.style.ERROR("Book extraction failed"))
        else:
            if options['force']:
                self.stdout.write("🔧 FORCE MODE: Extracting all books")
                results = extractor.extract_all_books(force_all=True)
            else:
                self.stdout.write("🔍 SMART MODE: Detecting new/unextracted books")
                results = extractor.extract_all_books(force_all=False)
            
            self._print_results(results)
    
    def _print_results(self, results):
        success_count = sum(1 for r in results if r['status'] == 'success')
        total_count = len(results)
        
        self.stdout.write(f"\n📊 Extraction Summary:")
        self.stdout.write(f"   ✅ Success: {success_count}")
        self.stdout.write(f"   ❌ Failed: {total_count - success_count}")
        self.stdout.write(f"   📚 Total: {total_count}")
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS("🎉 Extraction completed!"))
        else:
            self.stdout.write("📭 No books needed extraction")
    
    def _print_result(self, result):
        if result['status'] == 'success':
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ {result['book']} → {result['course_level']}: {result['size']} chars"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(f"❌ {result['book']}: {result['error']}")
            )
