"""
Lightweight services that replace PDF-dependent ones
"""
class LightweightAnswerService:
    def get_commentary(self, question):
        return "Study Bhagavad-gita As It Is by Srila Prabhupada for complete knowledge."
    
    def generate_choices(self, question):
        return [
            "Based on Bhagavad-gita teachings",
            "According to Vedic philosophy", 
            "As explained by Srila Prabhupada",
            "The scriptures provide the answer"
        ]

lightweight_service = LightweightAnswerService()
