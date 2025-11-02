import PyPDF2
import os
import re
from django.conf import settings

class BookExtractor:
    def __init__(self):
        self.books_base_dir = os.path.expanduser('~/Documents/Vaisnava books/book-app')
        self.extracted_dir = os.path.join(settings.BASE_DIR, 'extracted_books')
        os.makedirs(self.extracted_dir, exist_ok=True)
    
    def extract_all_books(self, force_all=False):
        """Extract books using exact filename matching"""
        results = []
        
        if not os.path.exists(self.books_base_dir):
            print(f"❌ Book directory not found: {self.books_base_dir}")
            return results
        
        print("📁 Extracting books with exact filename matching...")
        
        # Remove old extracted files
        if force_all:
            for old_file in os.listdir(self.extracted_dir):
                if old_file.endswith('.txt'):
                    os.remove(os.path.join(self.extracted_dir, old_file))
        
        # EXACT FILENAMES FROM YOUR FOLDER WITH COURSE MAPPING
        books_to_extract = {
            # BHAKTI SHASTRI
            'Bhagavad-gita-As-It-Is.pdf': 'bhakti_shastri',
            'sri-isopanisad.pdf': 'bhakti_shastri',
            'The_Nectar_of_Instruction-Original_1976_SCAN.pdf': 'bhakti_shastri',
            
            # BHAKTI VAIBAVA (Cantos 1-6)
            'Srimad-Bhagavatam_Canto_01.pdf': 'bhakti_vaibhava',
            'Srimad-Bhagavatam_Canto_02.pdf': 'bhakti_vaibhava', 
            'Srimad-Bhagavatam_Canto_03.pdf': 'bhakti_vaibhava',
            'Srimad-Bhagavatam_Canto_04.pdf': 'bhakti_vaibhava',
            'Srimad-Bhagavatam_Canto_05.pdf': 'bhakti_vaibhava',
            'Srimad-Bhagavatam_Canto_06.pdf': 'bhakti_vaibhava',
            '1. Srimad Bhagavata Mahapurana, 931 pgs.pdf': 'bhakti_vaibhava',
            
            # BHAKTI VEDANTA (Cantos 7-12)
            'Srimad-Bhagavatam_Canto_07.pdf': 'bhakti_vedanta',
            'Srimad-Bhagavatam_Canto_08.pdf': 'bhakti_vedanta',
            'Srimad-Bhagavatam_Canto_09.pdf': 'bhakti_vedanta',
            'Srimad-Bhagavatam_Canto_10.pdf': 'bhakti_vedanta',
            
            # BHAKTI SARVABHAUMA (Caitanya literature)
            'Chaitanya_Charitamrita_Compact-A_Summary_study_of_Sri_Chaitanya_Mahaprabhu\'s_life_story.pdf': 'bhakti_sarvabhauma',
            'Teachings_of_Lord_Chaitanya-1968_first_edition-SCAN.pdf': 'bhakti_sarvabhauma',
            'ant1.pdf': 'bhakti_sarvabhauma',
            'ant2.pdf': 'bhakti_sarvabhauma', 
            'ant3.pdf': 'bhakti_sarvabhauma',
            'ant4.pdf': 'bhakti_sarvabhauma',
            'ant5.pdf': 'bhakti_sarvabhauma',
            'mad3.pdf': 'bhakti_sarvabhauma',
            'mad4.pdf': 'bhakti_sarvabhauma',
            'mad5.pdf': 'bhakti_sarvabhauma',
            'mad6.pdf': 'bhakti_sarvabhauma',
            'mad7.pdf': 'bhakti_sarvabhauma',
            'mad8.pdf': 'bhakti_sarvabhauma',
            'mad9.pdf': 'bhakti_sarvabhauma',
            
            # SPANISH BOOKS
            'Nectar_de_la_devocion.pdf': 'spanish',
            'Srimad_Bhagavatam_Completo.pdf': 'spanish',
            'Nectar-of-Devotions-The-His-Divine-Grace-A.C.Bhaktivedanta-Swami-Prabhupada.pdf': 'spanish',
            'Caitanya_Caritamrta_Completo.pdf': 'spanish',
            'Bhagavad-gita_Tal_Como_Es_1978_condensed.pdf': 'spanish',
        }
        
        # Extract each specified book
        extracted_count = 0
        for filename, course_level in books_to_extract.items():
            pdf_path = os.path.join(self.books_base_dir, filename)
            
            if os.path.exists(pdf_path):
                print(f"✅ EXTRACTING: {filename} → {course_level}")
                result = self.extract_single_book(pdf_path, course_level)
                if result['status'] == 'success':
                    extracted_count += 1
                results.append(result)
            else:
                print(f"❌ NOT FOUND: {filename}")
                results.append({
                    'book': filename,
                    'course_level': course_level,
                    'status': 'error', 
                    'error': 'File not found'
                })
        
        print(f"🎯 Successfully extracted {extracted_count} out of {len(books_to_extract)} specified books")
        return results
    
    def extract_single_book(self, pdf_path, course_level):
        """Extract text from a single PDF book"""
        book_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        try:
            text = self._extract_pdf_text(pdf_path)
            cleaned_text = self._clean_extracted_text(text, book_name)
            
            # Save with course level
            safe_book_name = book_name.replace('/', '_').replace(' ', '_')
            output_path = os.path.join(self.extracted_dir, f"{course_level}_{safe_book_name}.txt")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            
            return {
                'book': book_name,
                'course_level': course_level,
                'status': 'success', 
                'path': output_path,
                'size': len(cleaned_text)
            }
            
        except Exception as e:
            return {
                'book': book_name,
                'course_level': course_level, 
                'status': 'error',
                'error': str(e)
            }
    
    def _extract_pdf_text(self, pdf_path):
        """Extract raw text from PDF"""
        text = ""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting {pdf_path}: {e}")
        return text
    
    def _clean_extracted_text(self, text, book_name):
        """Clean and organize extracted text"""
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text
