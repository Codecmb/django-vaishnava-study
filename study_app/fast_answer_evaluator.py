"""
Fast answer evaluator - no external dependencies
"""
import re

class FastAnswerEvaluator:
    def __init__(self):
        self.quality_indicators = [
            'krishna', 'bhagavad', 'gita', 'prabhupada', 'spiritual', 'soul', 'consciousness',
            'devotional', 'service', 'bhakti', 'yoga', 'verse', 'scripture', 'vedic'
        ]
    
    def evaluate_answer(self, question_text, user_answer):
        """Fast evaluation based on answer quality indicators"""
        if not user_answer or len(user_answer.strip()) < 5:
            return False, "Please provide a more substantial answer."
        
        answer_lower = user_answer.lower()
        word_count = len(answer_lower.split())
        
        # Check for quality indicators
        quality_score = sum(1 for indicator in self.quality_indicators if indicator in answer_lower)
        
        if word_count < 10:
            return False, "Please elaborate more in your answer."
        elif quality_score >= 2:
            return True, "Excellent answer! Shows good understanding of the philosophy."
        elif quality_score >= 1:
            return True, "Good answer. Continue your spiritual studies."
        else:
            return False, "Please study the Bhagavad-gita more carefully for this topic."
    
    def get_expected_guidance(self, question_text):
        """Provide guidance without external dependencies"""
        concepts = self.extract_concepts(question_text)
        if concepts:
            concept_str = ", ".join(concepts[:2])
            return f"Study the Bhagavad-gita's teachings about {concept_str} in Srila Prabhupada's purports."
        return "The complete knowledge can be found in Bhagavad-gita As It Is."
    
    def extract_concepts(self, text):
        """Extract key concepts from text"""
        stop_words = {'what', 'who', 'where', 'when', 'why', 'how', 'explain', 'describe', 'list'}
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        return [word for word in words if word not in stop_words]

# Global instance
fast_evaluator = FastAnswerEvaluator()
