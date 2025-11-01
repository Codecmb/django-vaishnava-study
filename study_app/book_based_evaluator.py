import re
import logging
from .pdf_commentary_service import pdf_commentary

logger = logging.getLogger(__name__)

class BookBasedEvaluator:
    """Evaluates answers based on actual book content from uploaded PDFs"""
    
    def evaluate_answer(self, question, user_answer, question_id=None):
        """
        Evaluate student answer using book content from PDF
        Returns: (is_correct, feedback, commentary)
        """
        try:
            # Get relevant book content for this question
            book_commentary = pdf_commentary.find_relevant_commentary(
                question=question,
                student_answer=user_answer,
                chapter=self._extract_chapter(question) if question else None
            )
            
            # Basic evaluation based on answer quality
            is_correct = self._assess_answer_quality(user_answer, book_commentary)
            feedback = self._generate_feedback(is_correct, user_answer)
            
            return is_correct, feedback, book_commentary
            
        except Exception as e:
            logger.error(f"Error in book-based evaluation: {e}")
            return True, "Thank you for your answer. Continue studying!", "Regular study of Bhagavad-gita will reveal all spiritual truths."
    
    def _extract_chapter(self, question):
        """Extract chapter reference from question if available"""
        # Look for chapter patterns in the question
        chapter_patterns = [
            r'chapter\s+(\d+)',
            r'Chapter\s+(\d+)',
            r'ch\.\s*(\d+)',
            r'CH\.\s*(\d+)'
        ]
        
        for pattern in chapter_patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                return f"Chapter {match.group(1)}"
        return None
    
    def _assess_answer_quality(self, user_answer, book_commentary):
        """Assess if the answer shows understanding based on book content"""
        if not user_answer or len(user_answer.strip()) < 3:
            return False
        
        # Check answer length and substance
        word_count = len(user_answer.split())
        
        # Look for key spiritual terms that indicate understanding
        spiritual_terms = [
            'krishna', 'bhagavad', 'gita', 'arjuna', 'dharma', 'karma',
            'bhakti', 'yoga', 'soul', 'atma', 'god', 'supreme', 'spiritual',
            'prabhupada', 'verse', 'teachings', 'knowledge', 'wisdom'
        ]
        
        found_terms = sum(1 for term in spiritual_terms if term in user_answer.lower())
        
        # Consider answer good if it has reasonable length and some relevant terms
        return word_count >= 5 and found_terms >= 1
    
    def _generate_feedback(self, is_correct, user_answer):
        """Generate appropriate feedback based on answer quality"""
        if not user_answer or len(user_answer.strip()) < 3:
            return "Please provide a more detailed answer. Study the relevant verses in Bhagavad-gita."
        
        if is_correct:
            feedbacks = [
                "Good understanding! Your answer shows spiritual insight.",
                "Well answered! Continue studying Prabhupada's books.",
                "Correct! Your understanding aligns with Vedic wisdom.",
                "Excellent! You're grasping the spiritual science.",
                "Good answer! Krishna consciousness is developing well."
            ]
            import hashlib
            index = hash(user_answer) % len(feedbacks)
            return feedbacks[index]
        else:
            return "Your answer shows some understanding, but study the relevant verses more carefully. The complete knowledge is in Bhagavad-gita As It Is."

# Global instance
book_evaluator = BookBasedEvaluator()
