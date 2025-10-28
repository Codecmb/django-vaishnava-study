import re

# Read the models.py file
with open('./study_app/models.py', 'r') as f:
    content = f.read()

# Find the QuizQuestion class and add the check_answer method
method_to_add = '''
    def check_answer(self, user_answer):
        """Check if user answer is correct"""
        import json
        if not user_answer or not self.correct_answers:
            return False
        
        # For multiple choice answers (numeric values)
        if user_answer.isdigit():
            try:
                choices = json.loads(self.multiple_choice_options)
                selected_choice = choices[int(user_answer)]
                return selected_choice == self.correct_answers
            except:
                return False
        
        # For written answers (text comparison)
        user_answer_clean = user_answer.strip().lower()
        correct_answers_clean = self.correct_answers.strip().lower()
        
        # Simple contains check for written answers
        return user_answer_clean in correct_answers_clean or correct_answers_clean in user_answer_clean
'''

# Find where to insert the method (after get_choices_list)
if 'def get_choices_list(self):' in content:
    # Find the end of get_choices_list method
    start_pos = content.find('def get_choices_list(self):')
    end_pos = content.find('\\n\\n', start_pos)  # Find double newline after method
    
    if end_pos != -1:
        # Insert check_answer method after get_choices_list
        content = content[:end_pos] + method_to_add + content[end_pos:]
        print("✓ Added check_answer method to QuizQuestion model")
    else:
        print("✗ Could not find where to insert method")
else:
    print("✗ Could not find get_choices_list method")

with open('./study_app/models.py', 'w') as f:
    f.write(content)
