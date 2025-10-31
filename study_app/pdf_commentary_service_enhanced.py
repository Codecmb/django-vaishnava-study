import pdfplumber
import os
import re
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class EnhancedPDFCommentaryService:
    """Enhanced PDF service using pdfplumber (better text extraction)"""
    
    def __init__(self):
        # PDF loading disabled for performance
        self.pdf_content = {}
        # self.load_pdf_content()  # Disabled for performance
    
    def load_pdf_content(self):
        """Load content from uploaded PDF books using pdfplumber"""
        try:
            from .models import BookPDF
            pdf_uploads = BookPDF.objects.all()
            
            for pdf_upload in pdf_uploads:
                if pdf_upload.pdf_file and os.path.exists(pdf_upload.pdf_file.path):
                    content = self._extract_pdf_text(pdf_upload.pdf_file.path)
                    book_title = pdf_upload.book.title.lower()
                    self.pdf_content[book_title] = content
                    logger.info(f"Loaded PDF content for: {book_title}")
                    
        except Exception as e:
            logger.error(f"Error loading PDF content: {e}")
    
    def _extract_pdf_text(self, pdf_path):
        """Extract text from PDF file using pdfplumber (better extraction)"""
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF text from {pdf_path}: {e}")
            return ""
    
    # Keep the rest of the methods the same as the original service
    def find_relevant_commentary(self, question, student_answer, chapter=None):
        """Find relevant Prabhupada commentary from PDF"""
        # ... (same implementation as original)
        pass

# Global instance
enhanced_pdf_commentary = EnhancedPDFCommentaryService()
