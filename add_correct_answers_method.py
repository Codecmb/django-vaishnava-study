# Read the models.py file
with open('./study_app/models.py', 'r') as f:
    content = f.read()

# Add the missing method to QuizQuestion class
method_to_add = '''
    def get_correct_answers_list(self):
        """Return correct answers as a list"""
        if not self.correct_answers:
            return []
        # Split by comma and strip whitespace
        return [answer.strip() for answer in self.correct_answers.split(',')]
'''

# Find the QuizQuestion class and add the method before the closing
import re
# Find after the last method in QuizQuestion
pattern = r'(def check_answer.*?return user_answer_clean in correct_answers_clean or correct_answers_clean in user_answer_clean\\n)'

def add_method(match):
    return match.group(1) + method_to_add

content = re.sub(pattern, add_method, content, flags=re.DOTALL)

with open('./study_app/models.py', 'w') as f:
    f.write(content)

print("✓ Added get_correct_answers_list method to QuizQuestion")
