"""
Intelligent Answer Generator that understands question types
"""
import json
import re
from .models import BookPDF, QuizQuestion

class IntelligentAnswerGenerator:
    def __init__(self, book_pdf):
        self.book_pdf = book_pdf
        self.text = book_pdf.extracted_text if book_pdf.text_extracted else ""
    
    def analyze_question_type(self, question_text):
        """Determine what type of answer the question needs"""
        question_lower = question_text.lower()
        
        if any(word in question_lower for word in ['list', 'symptoms', 'six', 'characteristics']):
            return "list_symptoms"
        elif any(word in question_lower for word in ['explain', 'analogy', 'meaning']):
            return "explanation"
        elif any(word in question_lower for word in ['why', 'reason', 'purpose']):
            return "reason"
        elif any(word in question_lower for word in ['what', 'define']):
            return "definition"
        else:
            return "general"
    
    def generate_appropriate_answers(self, question_text, chapter, question_type):
        """Generate answers that actually match the question type"""
        if question_type == "list_symptoms":
            return self.generate_symptom_answers(question_text, chapter)
        elif question_type == "explanation":
            return self.generate_explanation_answers(question_text, chapter)
        elif question_type == "reason":
            return self.generate_reason_answers(question_text, chapter)
        elif question_type == "definition":
            return self.generate_definition_answers(question_text, chapter)
        else:
            return self.generate_general_answers(question_text, chapter)
    
    def generate_symptom_answers(self, question_text, chapter):
        """Generate answers for 'list symptoms' type questions"""
        # These are actual symptoms of Bhagavan from Vedic scriptures
        correct_symptoms = [
            "All wealth (aisvarya)",
            "All strength (bala)",
            "All fame (yasas)",
            "All beauty (sri)",
            "All knowledge (jnana)",
            "All renunciation (vairagya)",
            "Has a transcendental form (sac-cid-ananda-vigraha)",
            "Has inconceivable energies (acintya-sakti)",
            "Can perform miracles (vismaya-karma)",
            "Is the source of all incarnations (avatari)"
        ]
        
        # Mix correct symptoms with plausible distractors
        distractors = [
            "Has a material body like humans",
            "Is subject to birth and death",
            "Has limited knowledge",
            "Can be defeated by demons",
            "Depends on devotees for existence",
            "Is a created being",
            "Has changing opinions",
            "Can make mistakes"
        ]
        
        import random
        answers = random.sample(correct_symptoms, 3)  # 3 correct options
        answers.extend(random.sample(distractors, 1))  # 1 wrong option
        random.shuffle(answers)
        return answers
    
    def find_relevant_commentary(self, question_text, chapter):
        """Find actual Prabhupada commentary relevant to the question"""
        if not self.text:
            return "The spiritual master is essential for understanding transcendental knowledge."
        
        # Search for relevant sections in the text
        keywords = self.extract_keywords(question_text)
        paragraphs = [p.strip() for p in self.text.split('\n\n') if p.strip()]
        
        for para in paragraphs:
            para_lower = para.lower()
            if any(keyword in para_lower for keyword in keywords):
                if len(para) > 50 and len(para) < 500:  # Reasonable length
                    return para
        
        return "Study Bhagavad-gita As It Is carefully under proper guidance."
    
    def extract_keywords(self, question_text):
        """Extract meaningful keywords"""
        stop_words = {'what', 'who', 'where', 'when', 'why', 'how', 'explain', 'list', 'describe'}
        words = re.findall(r'\b\w+\b', question_text.lower())
        return [word for word in words if word not in stop_words and len(word) > 3]
    
    def generate_personalized_guidance(self, question_text, user_answer, is_correct):
        """Generate personalized guidance based on the answer"""
        if is_correct:
            guidance_options = [
                "Excellent understanding! You've grasped the essential point.",
                "Very good! Your answer shows proper comprehension of the subject.",
                "Perfect! This demonstrates good study of the scriptures.",
                "Well done! Your answer reflects proper guidance from the spiritual master."
            ]
        else:
            guidance_options = [
                "Review the relevant verses in Bhagavad-gita for this topic.",
                "This concept is explained clearly in Srila Prabhupada's purports.",
                "Consider discussing this with an experienced devotee for clarity.",
                "Regular study and chanting will help internalize this knowledge."
            ]
        
        import random
        return random.choice(guidance_options)

def fix_question_answers(question_id):
    """Fix a specific question with intelligent answers"""
    try:
        question = QuizQuestion.objects.get(id=question_id)
        book_pdf = BookPDF.objects.filter(book=question.book).first()
        
        if book_pdf:
            generator = IntelligentAnswerGenerator(book_pdf)
            
            # Analyze question type
            question_type = generator.analyze_question_type(question.question_text)
            print(f"Question type: {question_type}")
            
            # Generate appropriate answers
            new_answers = generator.generate_appropriate_answers(
                question.question_text,
                question.chapter,
                question_type
            )
            
            # Update the question
            question.multiple_choice_options = json.dumps(new_answers)
            
            # Add relevant Prabhupada commentary if missing
            if not question.prabhupada_commentary:
                question.prabhupada_commentary = generator.find_relevant_commentary(
                    question.question_text, question.chapter
                )
            
            question.save()
            
            print(f"Fixed question {question_id}")
            print(f"New answers: {new_answers}")
            return True
            
    except Exception as e:
        print(f"Error fixing question {question_id}: {e}")
        return False
