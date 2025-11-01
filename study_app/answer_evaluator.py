"""
Intelligent Answer Evaluator for Vaishnava Study App
"""
import re

class AnswerEvaluator:
    def __init__(self):
        # Expected answers for specific questions
        self.expected_answers = {
            # Question 22: List six symptoms of Bhagavan
            22: {
                "type": "list_symptoms",
                "keywords": ["wealth", "aisvarya", "strength", "bala", "fame", "yasas",
                            "beauty", "sri", "knowledge", "jnana", "renunciation", "vairagya"],
                "required_count": 3
            },
            # Question 42: Krishna consciousness misunderstanding
            42: {
                "type": "misunderstanding",
                "keywords": ["impersonal", "voidism", "mayavada", "atheism", "materialism",
                            "speculation", "mental", "yoga", "meditation"],
                "required_count": 1
            },
            # Add more questions as needed
        }
        
        # Fallback expected answers for display
        self.fallback_expected = {
            22: "The six symptoms of Bhagavan are: 1) All wealth (aisvarya), 2) All strength (bala), 3) All fame (yasas), 4) All beauty (sri), 5) All knowledge (jnana), 6) All renunciation (vairagya)",
            42: "Krishna consciousness is sometimes misunderstood as: 1) Impersonal voidism or mayavada, 2) Materialistic philosophy, 3) Mental speculation, 4) Another form of yoga or meditation without devotion"
        }
    
    def evaluate_answer(self, question_id, user_answer):
        """Evaluate answer based on question type"""
        user_answer_lower = user_answer.lower().strip()
        
        # Handle empty answers
        if not user_answer_lower:
            return False, "Please provide an answer."
        
        # Check for specific question patterns
        if question_id in self.expected_answers:
            config = self.expected_answers[question_id]
            keywords = config["keywords"]
            required_count = config["required_count"]
            
            matches = sum(1 for keyword in keywords if keyword in user_answer_lower)
            
            if matches >= required_count:
                return True, f"Correct! Found {matches} relevant concepts."
            else:
                return False, f"Found {matches} relevant concepts. Need at least {required_count}."
        
        # Generic evaluation for other questions
        word_count = len(user_answer_lower.split())
        
        if word_count < 2:
            return False, "Please provide a more detailed answer."
        elif word_count < 5:
            return False, "Good start. Try to elaborate more on your answer."
        else:
            return True, "Good answer! Your understanding is developing well."
    
    def get_expected_answer(self, question_id):
        """Get the expected answer for display"""
        return self.fallback_expected.get(question_id, "Study the relevant verses in Bhagavad-gita for the correct understanding.")
