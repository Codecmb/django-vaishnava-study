# Read the models.py file
with open('./study_app/models.py', 'r') as f:
    lines = f.readlines()

# Find the QuizQuestion class and add the method at the end
in_quiz_class = False
quiz_class_end = None

for i, line in enumerate(lines):
    if 'class QuizQuestion' in line:
        in_quiz_class = True
    elif in_quiz_class and line.startswith('class ') and 'QuizQuestion' not in line:
        quiz_class_end = i
        break
    elif in_quiz_class and i == len(lines) - 1:
        quiz_class_end = i + 1

if quiz_class_end is not None:
    # Add the check_answer method
    method_code = [
        '\\n',
        '    def check_answer(self, user_answer):\\n',
        '        """Check if user answer is correct"""\\n',
        '        import json\\n',
        '        if not user_answer or not self.correct_answers:\\n',
        '            return False\\n',
        '        \\n',
        '        # For multiple choice answers (numeric values)\\n',
        '        if user_answer.isdigit():\\n',
        '            try:\\n',
        '                choices = json.loads(self.multiple_choice_options)\\n',
        '                selected_choice = choices[int(user_answer)]\\n',
        '                return selected_choice == self.correct_answers\\n',
        '            except:\\n',
        '                return False\\n',
        '        \\n',
        '        # For written answers (text comparison)\\n',
        '        user_answer_clean = user_answer.strip().lower()\\n',
        '        correct_answers_clean = self.correct_answers.strip().lower()\\n',
        '        \\n',
        '        # Simple contains check for written answers\\n',
        '        return user_answer_clean in correct_answers_clean or correct_answers_clean in user_answer_clean\\n',
        '\\n'
    ]
    
    lines[quiz_class_end:quiz_class_end] = method_code
    
    with open('./study_app/models.py', 'w') as f:
        f.writelines(lines)
    
    print("✓ Successfully added check_answer method to QuizQuestion model")
else:
    print("✗ Could not find QuizQuestion class")
