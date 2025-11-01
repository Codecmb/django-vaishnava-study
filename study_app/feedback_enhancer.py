"""
Feedback Enhancer - Makes existing AI responses more student-friendly
without changing the working core system
"""
import random

class FeedbackEnhancer:
    def __init__(self):
        self.engagement_boosters = {
            'starters': [
                "🌟 ", "💫 ", "📚 ", "🕉️ ", "🙏 ", "💖 ", "🎯 ", "🔍 ", "💡 ", "🌈 "
            ],
            'correct_celebrations': [
                "Excellent! ", "Fantastic! ", "Brilliant! ", "Perfect! ", 
                "Well done! ", "Great job! ", "You got it! ", "Spot on! "
            ],
            'encouragements': [
                "Keep studying Srila Prabhupada's books - you're making wonderful progress!",
                "Your spiritual understanding is growing beautifully!",
                "This knowledge will help you advance in Krishna consciousness!",
                "Regular study and chanting will deepen these realizations!",
                "You're building a strong foundation in spiritual science!",
                "Each correct understanding brings you closer to Krishna!"
            ],
            'compassionate_nudges': [
                "Spiritual understanding develops gradually - every attempt is valuable!",
                "Krishna consciousness is a journey, and you're on the right path!",
                "Don't worry - even great devotees had questions along the way!",
                "The beautiful thing about spiritual knowledge is that it grows with practice!",
                "Your sincerity in learning is what matters most to Krishna!"
            ]
        }
    
    def enhance_commentary(self, original_commentary):
        """Make Prabhupada commentary more engaging"""
        starter = random.choice(self.engagement_boosters['starters'])
        return f"{starter}{original_commentary}"
    
    def enhance_guidance(self, original_guidance, is_correct, user_answer):
        """Make guidance more personalized and encouraging"""
        if is_correct:
            celebration = random.choice(self.engagement_boosters['correct_celebrations'])
            encouragement = random.choice(self.engagement_boosters['encouragements'])
            return f"{celebration}{original_guidance} {encouragement}"
        else:
            # For incorrect answers, keep the original corrective guidance but add encouragement
            nudge = random.choice(self.engagement_boosters['compassionate_nudges'])
            return f"{original_guidance} {nudge}"
    
    def add_visual_elements(self, feedback_data):
        """Add simple visual indicators to feedback"""
        if feedback_data['is_correct']:
            feedback_data['visual_indicator'] = '✅'
            feedback_data['mood'] = 'celebratory'
        else:
            feedback_data['visual_indicator'] = '💡'
            feedback_data['mood'] = 'encouraging'
        
        return feedback_data

# Global enhancer instance
enhancer = FeedbackEnhancer()

def enhance_ai_feedback(original_feedback):
    """
    Enhance existing AI feedback to be more student-friendly
    without changing the core functionality
    """
    enhanced_feedback = original_feedback.copy()
    
    # Enhance commentary with engaging starters
    enhanced_feedback['prabhupada_commentary'] = enhancer.enhance_commentary(
        original_feedback['prabhupada_commentary']
    )
    
    # Enhance guidance with personalized encouragement
    enhanced_feedback['additional_guidance'] = enhancer.enhance_guidance(
        original_feedback['additional_guidance'],
        original_feedback['is_correct'],
        'user_answer_placeholder'  # We don't have user_answer in this context
    )
    
    # Add visual elements
    enhanced_feedback = enhancer.add_visual_elements(enhanced_feedback)
    
    return enhanced_feedback
