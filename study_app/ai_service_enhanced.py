"""
Enhanced AI Service Wrapper - Uses existing AI service but makes output more engaging
"""
from study_app.ai_service import get_ai_feedback
from study_app.feedback_enhancer import enhance_ai_feedback

def get_enhanced_ai_feedback(question_text, user_answer, correct_answers, verse_reference=None):
    """
    Get AI feedback with enhanced student engagement
    Uses the existing working system but makes output more attractive
    """
    # Get the original working feedback
    original_feedback = get_ai_feedback(question_text, user_answer, correct_answers, verse_reference)
    
    # Enhance it for better student engagement
    enhanced_feedback = enhance_ai_feedback(original_feedback)
    
    return enhanced_feedback
