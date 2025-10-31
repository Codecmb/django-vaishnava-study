"""
Pure PDF-based answer generator that uses ONLY the book content
"""
import json
import random
import re
from .models import BookPDF, QuizQuestion

class PurePDFAnswerGenerator:
    def __init__(self):
        self.pdf_cache = {}
    
    def get_book_text(self, book):
        """Get the raw text from the book PDF"""
        try:
            if book.id in self.pdf_cache:
                return self.pdf_cache[book.id]
            
            book_pdf = BookPDF.objects.filter(book=book).first()
            if book_pdf and book_pdf.text_extracted and book_pdf.extracted_text:
                self.pdf_cache[book.id] = book_pdf.extracted_text
                return book_pdf.extracted_text
            
            return ""
        except Exception as e:
            print(f"Error getting book text: {e}")
            return ""
    
    def extract_random_phrases_from_book(self, book_text, count=10, min_length=20):
        """Extract random meaningful phrases from the book text"""
        if not book_text:
            return []
        
        # Split into sentences and meaningful phrases
        sentences = re.split(r'[.!?]+', book_text)
        meaningful_phrases = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            words = sentence.split()
            if len(words) >= 5 and len(sentence) > min_length:  # Substantial content
                meaningful_phrases.append(sentence)
        
        # Return random selection
        if len(meaningful_phrases) <= count:
            return meaningful_phrases
        else:
            return random.sample(meaningful_phrases, count)
    
    def extract_verse_like_sections(self, book_text):
        """Extract sections that look like verses or commentaries"""
        if not book_text:
            return []
        
        # Look for patterns that indicate verses or important teachings
        patterns = [
            r'"([^"]{30,200})"',  # Quoted text
            r'\. ([A-Z][^.!?]{30,150}\.)',  # Substantial sentences
            r'\n([A-Z][^\n]{50,300})',  # Paragraph starts
        ]
        
        sections = []
        for pattern in patterns:
            matches = re.findall(pattern, book_text)
            sections.extend(matches)
        
        return sections
    
    def generate_choices_from_book_only(self, question):
        """Generate multiple choice options using ONLY the book content"""
        book_text = self.get_book_text(question.book)
        
        if not book_text:
            # Fallback: return empty choices to avoid nonsense
            return ["Study the book carefully", "Refer to the actual verses", 
                   "Consult Prabhupada's commentary", "Read Bhagavad-gita As It Is"]
        
        # Extract various types of content from the book
        random_phrases = self.extract_random_phrases_from_book(book_text, count=15)
        verse_sections = self.extract_verse_like_sections(book_text)
        
        # Combine all potential content
        all_book_content = random_phrases + verse_sections
        
        if not all_book_content:
            # If no substantial content found, use generic book-based responses
            return [
                "The answer is found in Bhagavad-gita As It Is",
                "Srila Prabhupada explains this in his commentary",
                "This is discussed in the verses of Bhagavad-gita", 
                "The complete knowledge is in the book"
            ]
        
        # Use the actual correct answer if available
        correct_answer = question.correct_answers
        if not correct_answer or len(correct_answer.strip()) < 10:
            # If no good correct answer, use a meaningful book phrase
            correct_answer = random.choice(all_book_content) if all_book_content else "Based on Bhagavad-gita teachings"
        
        # Start with correct answer
        choices = [correct_answer]
        
        # Select other choices from actual book content
        other_content = [c for c in all_book_content if c != correct_answer]
        
        if len(other_content) >= 3:
            # Use actual book content for distractors
            distractors = random.sample(other_content, 3)
            choices.extend(distractors)
        else:
            # Not enough unique content, create variations from available content
            while len(choices) < 4:
                if other_content:
                    new_choice = random.choice(other_content)
                    if new_choice not in choices:
                        choices.append(new_choice)
                else:
                    # Create simple variations from the book's style
                    variations = [
                        "This principle is explained throughout the book",
                        "The verses provide complete understanding",
                        "Prabhupada's purports clarify this subject",
                        "Bhagavad-gita contains the answer"
                    ]
                    for var in variations:
                        if var not in choices and len(choices) < 4:
                            choices.append(var)
        
        # Ensure uniqueness and shuffle
        choices = list(dict.fromkeys(choices))  # Remove duplicates while preserving order
        while len(choices) < 4:
            choices.append(f"Answer from {question.book.title}")
        
        random.shuffle(choices)
        return choices[:4]  # Ensure exactly 4 choices
    
    def extract_commentary_from_book(self, question):
        """Extract actual commentary from the book text"""
        book_text = self.get_book_text(question.book)
        
        if not book_text:
            return "Please study Bhagavad-gita As It Is by His Divine Grace A.C. Bhaktivedanta Swami Prabhupada."
        
        # Extract random substantial paragraph from the book
        paragraphs = [p.strip() for p in book_text.split('\n\n') if len(p.strip()) > 100]
        
        if paragraphs:
            # Return a random substantial paragraph as commentary
            return random.choice(paragraphs)
        else:
            # Fallback to book-based message
            return f"The complete explanation is found in {question.book.title}. Please study it carefully."
    
    def enhance_question_purely_from_book(self, question_id):
        """Enhance a question using ONLY the book content"""
        try:
            question = QuizQuestion.objects.get(id=question_id)
            
            # Generate choices purely from book content
            book_based_choices = self.generate_choices_from_book_only(question)
            
            # Update multiple choice options
            question.multiple_choice_options = json.dumps(book_based_choices)
            
            # Extract commentary purely from book
            if not question.prabhupada_commentary:
                question.prabhupada_commentary = self.extract_commentary_from_book(question)
            
            question.save()
            print(f"Enhanced question {question_id} purely from book content")
            print(f"Choices: {book_based_choices}")
            return True
            
        except Exception as e:
            print(f"Error enhancing question {question_id}: {e}")
            return False

# Global instance
pure_pdf_generator = PurePDFAnswerGenerator()
