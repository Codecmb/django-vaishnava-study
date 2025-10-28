# Read the current file
with open('./study_app/models.py', 'r') as f:
    content = f.read()

# Find and fix any issues with QuizAttempt class
# Look for the QuizAttempt class definition
import re

# Check if QuizAttempt class exists and is properly defined
if 'class QuizAttempt' not in content:
    # Add missing QuizAttempt class
    quizattempt_code = '''
class QuizAttempt(models.Model):
    """Track user quiz attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    module = models.ForeignKey(QuizModule, on_delete=models.CASCADE)
    answers = models.JSONField(default=dict)  # Stores {question_id: user_answer}
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_score(self):
        """Calculate score for this attempt"""
        score = 0
        for question_id, user_answer in self.answers.items():
            try:
                question = QuizQuestion.objects.get(id=question_id)
                if question.check_answer(user_answer):
                    score += 1
            except QuizQuestion.DoesNotExist:
                continue
        self.score = score
        self.total_questions = len(self.answers)
        self.save()
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.book.title} - Score: {self.score}/{self.total_questions}"
'''
    
    # Add after QuizQuestion class
    quizquestion_end = content.find('class QuizQuestion')
    if quizquestion_end != -1:
        # Find the end of QuizQuestion class
        next_class = content.find('class ', quizquestion_end + 1)
        if next_class == -1:
            next_class = len(content)
        content = content[:next_class] + quizattempt_code + content[next_class:]
        print("✓ Added missing QuizAttempt class")
    else:
        print("✗ Could not find where to add QuizAttempt class")

with open('./study_app/models.py', 'w') as f:
    f.write(content)
