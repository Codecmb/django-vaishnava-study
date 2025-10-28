with open('./study_app/templates/study_app/take_quiz.html', 'r') as f:
    content = f.read()

# Remove the validation-area div that contains the Check Siddhanta button
import re
pattern = r'<div class="validation-area">.*?<button.*?</button>.*?</div>'
content = re.sub(pattern, '', content, flags=re.DOTALL)

with open('./study_app/templates/study_app/take_quiz.html', 'w') as f:
    f.write(content)

print("✓ Removed Check Siddhanta button")
