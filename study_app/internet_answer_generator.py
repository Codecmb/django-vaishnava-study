"""
Internet-based answer generator - optimized for speed
"""
import json
import random

class InternetAnswerGenerator:
    def __init__(self):
        # Lightweight initialization - no heavy imports
        self.answer_templates = {
            'philosophical': [
                "According to Vedic philosophy, {concept} is understood as",
                "The Bhagavad-gita teaches that {concept} means",
                "Srila Prabhupada explains {concept} in his commentaries as",
                "In Krishna consciousness, {concept} refers to"
            ]
        }
    
    def extract_concept_from_question(self, question_text):
        """Extract the main concept from the question"""
        question_words = ['what', 'who', 'where', 'when', 'why', 'how', 'explain', 'describe', 'list']
        words = question_text.lower().split()
        concepts = [word for word in words if word not in question_words and len(word) > 3]
        return ' '.join(concepts[:3]) if concepts else "spiritual knowledge"
    
    def generate_meaningful_choices(self, question):
        """Generate meaningful choices - optimized version"""
        concept = self.extract_concept_from_question(question.question_text)
        
        # Use actual correct answer if available
        correct_answer = question.correct_answers
        if not correct_answer or len(correct_answer.strip()) < 10:
            template = random.choice(self.answer_templates['philosophical'])
            correct_answer = template.format(concept=concept) + " a transcendental reality."
        
        # Fast distractors generation
        distractors = [
            f"{concept.title()} is a material concept",
            f"The modern view of {concept} differs",
            f"{concept.title()} can be understood mentally",
            f"{concept.title()} is subject to interpretation"
        ]
        
        choices = [correct_answer] + random.sample(distractors, 3)
        random.shuffle(choices)
        return choices
    
    def generate_commentary(self, question):
        """Generate fast commentary"""
        concept = self.extract_concept_from_question(question.question_text)
        return f"Study Bhagavad-gita As It Is to understand {concept} properly."

# Global instance - lightweight
internet_generator = InternetAnswerGenerator()
