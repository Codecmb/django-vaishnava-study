import PyPDF2
import os
import re
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class PDFCommentaryService:
    """Service to extract authentic Prabhupada commentaries from uploaded PDF books"""
    
    def __init__(self):
        self.pdf_content = {}
        self.load_pdf_content()
    
    def load_pdf_content(self):
        """Load content from uploaded PDF books"""
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
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting PDF text from {pdf_path}: {e}")
            return ""
    
    def find_relevant_commentary(self, question, student_answer, chapter=None):
        """Find relevant Prabhupada commentary from PDF based on question and answer"""
        try:
            # Search in Bhagavad-gita content first
            bg_content = self.pdf_content.get('bhagavad-gita', '')
            if not bg_content:
                # Try to find any content with 'gita' in the title
                for title, content in self.pdf_content.items():
                    if 'gita' in title:
                        bg_content = content
                        break
            
            if bg_content:
                return self._extract_bg_commentary(bg_content, question, student_answer, chapter)
            else:
                return self._get_fallback_commentary(question, student_answer)
                
        except Exception as e:
            logger.error(f"Error finding commentary: {e}")
            return self._get_fallback_commentary(question, student_answer)
    
    def _extract_bg_commentary(self, content, question, student_answer, chapter):
        """Extract Bhagavad-gita specific commentary"""
        # Extract keywords from question
        keywords = self._extract_keywords(question, student_answer)
        
        # If chapter specified, search in that chapter
        if chapter:
            chapter_sections = self._extract_chapter_sections(content, chapter)
            if chapter_sections:
                relevant_text = self._find_most_relevant_section(chapter_sections, keywords)
                if relevant_text:
                    return f"From Bhagavad-gita {chapter}:\n\n{relevant_text}"
        
        # Fallback to general search
        paragraphs = re.split(r'\n\s*\n', content)
        relevant_paras = []
        
        for para in paragraphs:
            if len(para.strip()) > 50:
                score = sum(1 for keyword in keywords if keyword in para.lower())
                if score > 0:
                    relevant_paras.append((score, para))
        
        if relevant_paras:
            relevant_paras.sort(reverse=True)
            best_para = relevant_paras[0][1]
            if len(best_para) > 500:
                best_para = best_para[:500] + "..."
            return f"From Bhagavad-gita As It Is:\n\n{best_para}"
        else:
            return self._get_fallback_commentary(question, student_answer)
    
    def _extract_keywords(self, question, student_answer):
        """Extract relevant keywords from question and answer"""
        spiritual_terms = [
            'krishna', 'arjuna', 'bhagavad', 'gita', 'yoga', 'dharma', 'karma',
            'jnana', 'bhakti', 'sankhya', 'dhyana', 'brahman', 'atma', 'paramatma',
            'maya', 'prakriti', 'purusha', 'samsara', 'moksha', 'sannyasa',
            'varnashrama', 'guru', 'sastra', 'veda', 'upanishad', 'brahmana',
            'prabhupada', 'verse', 'chapter', 'bhagavan', 'supreme', 'lord'
        ]
        
        words = re.findall(r'\b[a-z]{4,}\b', (question + " " + student_answer).lower())
        keywords = [word for word in words if word in spiritual_terms or len(word) > 5]
        return list(set(keywords))
    
    def _extract_chapter_sections(self, content, chapter):
        """Extract sections for a specific chapter"""
        # Look for chapter patterns like "Chapter 1", "CHAPTER ONE", etc.
        chapter_patterns = [
            rf"chapter\s+{chapter}.*?(?=chapter\s+\d+|$)",
            rf"CHAPTER\s+{chapter}.*?(?=CHAPTER\s+\d+|$)",
            rf"chapter\s+{chapter}.*?(\n\n|$)"
        ]
        
        for pattern in chapter_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                return matches
        return []
    
    def _find_most_relevant_section(self, sections, keywords):
        """Find the most relevant section based on keywords"""
        scored_sections = []
        for section in sections:
            score = sum(1 for keyword in keywords if keyword in section.lower())
            if score > 0:
                scored_sections.append((score, section))
        
        if scored_sections:
            scored_sections.sort(reverse=True)
            return scored_sections[0][1][:1000]  # Limit length
        elif sections:
            return sections[0][:1000]
        return None
    
    def _get_fallback_commentary(self, question, student_answer):
        """Provide fallback commentary"""
        fallbacks = [
            "Study Bhagavad-gita As It Is carefully under the guidance of a spiritual master.",
            "As Srila Prabhupada writes, one should approach a bona fide spiritual master for transcendental knowledge.",
            "Regular chanting of Hare Krishna and studying Prabhupada's books will reveal the answers.",
            "The complete science of God is explained in Bhagavad-gita As It Is by His Divine Grace A.C. Bhaktivedanta Swami Prabhupada.",
            "Continue your spiritual studies with faith and determination in Krishna consciousness."
        ]
        import hashlib
        index = hash(question + student_answer) % len(fallbacks)
        return fallbacks[index]

# Global instance
pdf_commentary = PDFCommentaryService()
