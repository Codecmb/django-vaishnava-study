"""
English PDF-based Answer Generator
"""
import json
import re
import random
from .models import BookPDF, QuizQuestion

class EnglishAnswerGenerator:
    def __init__(self, book_pdf):
        self.book_pdf = book_pdf
        self.text = book_pdf.extracted_text if book_pdf.text_extracted else ""
    
    def find_relevant_content(self, question_text, chapter=None):
        """Find content relevant to the question"""
        if not self.text:
            return []
        
        keywords = self.extract_keywords(question_text)
        relevant_paragraphs = []
        
        paragraphs = [p.strip() for p in self.text.split('\n\n') if p.strip()]
        
        for para in paragraphs:
            para_lower = para.lower()
            score = 0
            
            # Score based on keyword matches
            for keyword in keywords:
                if keyword in para_lower:
                    score += 3
            
            # Bonus for chapter reference
            if chapter:
                chapter_indicators = [
                    f'chapter {chapter}',
                    f'chapter {chapter}.',
                    f'chapter {chapter}:',
                    f'chapter {chapter.lower()}'
                ]
                if any(indicator in para_lower for indicator in chapter_indicators):
                    score += 5
            
            if score > 0:
                relevant_paragraphs.append((para, score))
        
        # Return top 3 most relevant
        relevant_paragraphs.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in relevant_paragraphs[:3]]
    
    def extract_keywords(self, question_text):
        """Extract meaningful keywords from question"""
        stop_words = {
            'what', 'who', 'where', 'when', 'why', 'how', 'explain', 'list', 
            'describe', 'does', 'is', 'are', 'the', 'and', 'of', 'in', 'to'
        }
        
        words = re.findall(r'\b\w+\b', question_text.lower())
        return [word for word in words if word not in stop_words and len(word) > 3]
    
    def generate_contextual_answers(self, question_text, chapter=None, num_options=4):
        """Generate answers from English PDF content"""
        relevant_content = self.find_relevant_content(question_text, chapter)
        
        if not relevant_content:
            return self.get_philosophical_fallback_answers()
        
        answers = self.extract_answer_candidates(relevant_content)
        
        # Ensure we have enough unique answers
        unique_answers = list(dict.fromkeys(answers))
        while len(unique_answers) < num_options:
            new_fallback = self.get_philosophical_fallback_answers()
            unique_answers.extend([a for a in new_fallback if a not in unique_answers])
        
        random.shuffle(unique_answers)
        return unique_answers[:num_options]
    
    def extract_answer_candidates(self, content_paragraphs):
        """Extract potential answers from content"""
        candidates = []
        
        for para in content_paragraphs:
            # Extract meaningful sentences
            sentences = re.split(r'[.!?]', para)
            for sentence in sentences:
                sentence = sentence.strip()
                # Good answer candidates are medium-length, complete thoughts
                if (25 <= len(sentence) <= 150 and 
                    len(sentence.split()) >= 5 and
                    not sentence.startswith(('Chapter', 'CHAPTER', 'Verse'))):
                    candidates.append(sentence)
        
        return candidates
    
    def get_philosophical_fallback_answers(self):
        """Fallback answers based on Vedic philosophy"""
        return [
            "According to the teachings of Srila Prabhupada",
            "As explained in Vedic scriptures",
            "Based on the principles of Bhagavad-gita",
            "Through spiritual realization and practice",
            "According to the disciplic succession",
            "As per the Vedic cosmological understanding",
            "Based on the science of devotional service",
            "According to the eternal principles of sanatana-dharma"
        ]

def update_question_with_english_answers(question_id):
    """Update a question with English PDF-based answers"""
    try:
        question = QuizQuestion.objects.get(id=question_id)
        book_pdf = BookPDF.objects.filter(book=question.book).first()
        
        if book_pdf and book_pdf.text_extracted and book_pdf.extracted_text:
            generator = EnglishAnswerGenerator(book_pdf)
            new_answers = generator.generate_contextual_answers(
                question.question_text,
                question.chapter
            )
            
            question.multiple_choice_options = json.dumps(new_answers)
            question.save()
            print(f'Updated question {question_id}: {question.question_text[:50]}...')
            print(f'New answers: {new_answers}')
            return True
        else:
            print(f'No English text available for question {question_id}')
            return False
            
    except Exception as e:
        print(f'Error updating question {question_id}: {e}')
        return False

def update_all_questions_with_english_answers():
    """Update all questions with English PDF-based answers"""
    questions = QuizQuestion.objects.all()
    updated_count = 0
    
    for question in questions:
        try:
            book_pdf = BookPDF.objects.filter(book=question.book).first()
            
            if book_pdf and book_pdf.text_extracted and book_pdf.extracted_text:
                generator = EnglishAnswerGenerator(book_pdf)
                new_answers = generator.generate_contextual_answers(
                    question.question_text,
                    question.chapter
                )
                
                question.multiple_choice_options = json.dumps(new_answers)
                question.save()
                updated_count += 1
                print(f'✓ Updated question {question.id}')
            else:
                print(f'✗ No English text for question {question.id}')
                
        except Exception as e:
            print(f'✗ Error with question {question.id}: {e}')
    
    print(f'\nTotal questions updated: {updated_count}/{len(questions)}')
    return updated_count
