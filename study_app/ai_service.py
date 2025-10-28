"""
Real-time AI Service for generating Prabhupada commentary and feedback
No database storage - all generated on demand
"""
import random

class RealTimeAIService:
    def __init__(self):
        print("RealTimeAIService initialized - ready for real-time feedback")
        self.commentary_templates = {
            'krishna': [
                "Srila Prabhupada explains that Krishna is the Supreme Personality of Godhead, the source of all incarnations. In Bhagavad-gita, Krishna declares 'I am the source of all spiritual and material worlds. Everything emanates from Me.' (Bg. 10.8)",
                "Krishna is the origin of everything, as confirmed in Vedanta-sutra: janmady asya yatah. He is the supreme enjoyer, the proprietor of everything, and the best friend of all living entities.",
                "Prabhupada teaches that Krishna is sac-cid-ananda-vigraha - the eternal form of bliss and knowledge. Understanding Krishna's position is the beginning of spiritual realization."
            ],
            'bhakti': [
                "Devotional service, bhakti-yoga, is the eternal function of the soul. Prabhupada emphasizes that by engaging in nine processes of bhakti, especially hearing and chanting, one can revive original consciousness.",
                "The process of Krishna consciousness involves surrendering to Krishna and serving Him with love. As stated in Bhagavad-gita, 'Always think of Me, become My devotee, worship Me and offer your homage unto Me.' (Bg. 9.34)",
                "Bhakti is the only means to attain the Supreme Lord. Prabhupada explains that through sincere devotional service, one becomes purified and eligible to return to Krishna's eternal abode."
            ],
            'gita': [
                "Bhagavad-gita is the essence of all Vedic knowledge, spoken directly by Lord Krishna. Prabhupada's purports give the authorized explanation for this age.",
                "The Gita establishes that we are not these bodies but eternal spirit souls. As Krishna says, 'For the soul there is never birth nor death. He is eternal and never dies.' (Bg. 2.20)",
                "Prabhupada's Bhagavad-gita As It Is reveals the science of God and the process of devotional service. It is the perfect guide for spiritual life."
            ],
            'chanting': [
                "Chanting Hare Krishna is the recommended spiritual practice for this age. Prabhupada says this chanting cleanses the dust from the mirror of the mind.",
                "The holy name of Krishna is non-different from Krishna Himself. By sincerely chanting, one directly associates with the Supreme Lord.",
                "Prabhupada established the chanting of Hare Krishna as the prime means of deliverance in this Kali-yuga. It is the most merciful process given by Lord Chaitanya."
            ],
            'general': [
                "Srila Prabhupada's mission is to spread Krishna consciousness worldwide. His books provide the authorized explanation of Vedic wisdom.",
                "The spiritual master is essential for understanding transcendental knowledge. By his mercy, one receives the seed of devotional service.",
                "Krishna consciousness means to be always conscious of Krishna. This state is achieved by following the regulative principles and chanting regularly."
            ]
        }
        
        self.guidance_templates = {
            'correct': [
                "Excellent understanding! This shows good grasp of the philosophy. Continue studying Srila Prabhupada's books to deepen your realization.",
                "Very good! Your answer aligns with Vedic wisdom. Regular study will strengthen this understanding.",
                "Perfect! This knowledge comes from proper guidance. Keep associating with devotees and reading Prabhupada's books.",
                "Correct! Your understanding will help you advance in Krishna consciousness. Hare Krishna!"
            ],
            'incorrect': [
                "Thank you for your effort. Spiritual understanding develops gradually - keep studying and your realization will deepen.",
                "Good attempt! Don't be discouraged. Continue reading Srila Prabhupada's purports - they will clarify all philosophical points.",
                "Your sincerity is appreciated. Spiritual knowledge comes by the mercy of Krishna and the spiritual master.",
                "Nice try! Krishna consciousness is a progressive science. Regular practice will bring perfect understanding."
            ]
        }
    
    def _detect_topic(self, question_text):
        """Detect the main topic of the question for relevant commentary"""
        if not question_text:
            return 'general'
            
        question_lower = question_text.lower()
        
        if any(word in question_lower for word in ['krishna', 'god', 'supreme', 'lord', 'krsna']):
            return 'krishna'
        elif any(word in question_lower for word in ['bhakti', 'devotional', 'service', 'worship', 'devotee']):
            return 'bhakti'
        elif any(word in question_lower for word in ['gita', 'bhagavad', 'verse', 'scripture']):
            return 'gita'
        elif any(word in question_lower for word in ['chant', 'hare', 'mantra', 'mahamantra']):
            return 'chanting'
        else:
            return 'general'
    
    def generate_commentary(self, question_text, correct_answers, verse_reference=None):
        """Generate real-time Prabhupada commentary"""
        topic = self._detect_topic(question_text)
        templates = self.commentary_templates.get(topic, self.commentary_templates['general'])
        
        # Select random template and personalize it
        commentary = random.choice(templates)
        
        # Add verse reference if provided
        if verse_reference:
            commentary = f"In {verse_reference}, {commentary.lower()}"
        
        print(f"Generated commentary for topic '{topic}': {commentary[:50]}...")
        return commentary
    
    def generate_guidance(self, question_text, user_answer, is_correct, correct_answers):
        """Generate real-time additional guidance"""
        template_key = 'correct' if is_correct else 'incorrect'
        guidance = random.choice(self.guidance_templates[template_key])
        
        if not is_correct:
            guidance += f" The correct understanding is: {correct_answers}."
        
        print(f"Generated {template_key} guidance: {guidance[:50]}...")
        return guidance

# Global instance
ai_service = RealTimeAIService()

def generate_prabhupada_commentary(question_text, correct_answers, verse_reference=None):
    """
    Generate real-time Prabhupada commentary - no database storage
    """
    return ai_service.generate_commentary(question_text, correct_answers, verse_reference)

def generate_additional_guidance(question_text, user_answer, is_correct, correct_answers):
    """
    Generate real-time additional guidance - no database storage
    """
    return ai_service.generate_guidance(question_text, user_answer, is_correct, correct_answers)

def get_ai_feedback(question_text, user_answer, correct_answers, verse_reference=None):
    """
    Get comprehensive real-time AI feedback
    No database storage - generated fresh each time
    """
    print(f"Getting AI feedback for: {question_text}")
    
    # Generate commentary
    commentary = generate_prabhupada_commentary(question_text, correct_answers, verse_reference)
    
    # Determine correctness
    user_clean = str(user_answer).strip().lower() if user_answer else ""
    correct_clean = str(correct_answers).strip().lower() if correct_answers else ""
    is_correct = (user_clean in correct_clean or 
                  correct_clean in user_clean or 
                  user_clean == correct_clean)
    
    print(f"User answer: '{user_clean}', Correct: '{correct_clean}', Is correct: {is_correct}")
    
    # Generate guidance
    guidance = generate_additional_guidance(question_text, user_answer, is_correct, correct_answers)
    
    result = {
        'prabhupada_commentary': commentary,
        'additional_guidance': guidance,
        'is_correct': is_correct
    }
    
    print(f"AI Feedback result ready")
    return result
