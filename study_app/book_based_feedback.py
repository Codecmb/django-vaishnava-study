"""
Feedback system that uses ONLY the actual book content
"""
import random
from .pure_pdf_answer_generator import pure_pdf_generator

class BookBasedFeedback:
    def __init__(self):
        self.pdf_generator = pure_pdf_generator
    
    def generate_feedback_from_book(self, question, user_answer, is_correct):
        """Generate feedback using ONLY book content"""
        book_commentary = self.pdf_generator.extract_commentary_from_book(question)
        
        if is_correct:
            base = "Correct. "
        else:
            base = "Please review. "
        
        # Combine with actual book content
        feedback = base + "This is explained in the book: " + book_commentary[:200] + "..."
        
        return feedback
    
    def get_expected_answer_guidance(self, question):
        """Get guidance about where to find the answer in the book"""
        book_text = self.pdf_generator.get_book_text(question.book)
        
        if not book_text:
            return "The answer can be found by carefully studying Bhagavad-gita As It Is."
        
        # Extract a relevant-looking section
        paragraphs = [p.strip() for p in book_text.split('\n\n') if 50 < len(p.strip()) < 500]
        
        if paragraphs:
            guidance = random.choice(paragraphs)
            return f"Study this section from the book: {guidance[:300]}..."
        else:
            return "The complete knowledge is in Bhagavad-gita As It Is by Srila Prabhupada."

# Global instance
book_feedback = BookBasedFeedback()
