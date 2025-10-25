"""
Student Answer Processor - Populates correct_answers field after student input
"""

class StudentAnswerProcessor:
    def process_student_answer(self, question, student_answer, answer_type):
        """
        Process student answer and populate correct_answers field
        """
        # If correct_answers is already populated, keep it
        if question.correct_answers and question.correct_answers.strip():
            correct_answer = question.correct_answers
            was_populated = True
        else:
            # Auto-generate correct answer based on student input and question
            correct_answer = self.generate_correct_answer(question, student_answer, answer_type)
            was_populated = False
        
        # Generate Prabhupada commentary
        commentary = self.generate_commentary(question, student_answer, correct_answer, answer_type)
        
        return {
            'correct_answer': correct_answer,
            'prabhupada_commentary': commentary,
            'was_populated': was_populated,
            'should_save': not was_populated  # Only save if we're populating for the first time
        }
    
    def generate_correct_answer(self, question, student_answer, answer_type):
        """Generate the correct answer based on the question and student input"""
        
        # For multiple choice questions
        if answer_type == 'multiple_choice' and question.multiple_choice_options:
            # The correct answer is the selected multiple choice option
            return student_answer
        
        # For written answers about specific topics
        question_lower = question.question_text.lower()
        
        if 'soul' in question_lower or 'eternal' in question_lower:
            return "The soul is eternal, indestructible, and cannot be killed by any means. It simply changes bodies like changing clothes."
        
        elif 'bhakti' in question_lower or 'devotional' in question_lower:
            return "Bhakti-yoga is the process of devotional service to Lord Krishna, which is the eternal function of the soul."
        
        elif 'karma' in question_lower:
            return "Karma refers to material activities that bind the soul to the cycle of birth and death through the law of action and reaction."
        
        elif 'krishna' in question_lower or 'god' in question_lower:
            return "Krishna is the Supreme Personality of Godhead, the source of all incarnations and the ultimate goal of devotional service."
        
        else:
            # Generic correct answer based on the question
            return f"The answer can be found in {question.verse_reference}. Study Srila Prabhupada's commentary for complete understanding."
    
    def generate_commentary(self, question, student_answer, correct_answer, answer_type):
        """Generate Prabhupada commentary based on the correct answer"""
        
        base_commentary = f"""
As Srila Prabhupada explains in his commentary, this verse reveals important spiritual knowledge. 

The correct understanding is: {correct_answer}

This knowledge is essential for progressing in spiritual life and understanding our relationship with Krishna.
"""
        
        # Add specific feedback based on answer type
        if answer_type == 'multiple_choice':
            base_commentary += "\n\nMultiple choice questions help test basic understanding, but deep realization comes from careful study of the scriptures."
        else:
            base_commentary += "\n\nWritten answers allow you to express your understanding in your own words. Continue studying to deepen your realization."
        
        return base_commentary

# Global instance
student_processor = StudentAnswerProcessor()
