import re

with open('./study_app/templates/study_app/take_quiz.html', 'r') as f:
    content = f.read()

# Find the current multiple choice section and replace JUST the content
old_multiple_choice_content = '''                                <div class="multiple-choice-section">
                                    <h6>Select Your Answer:</h6>
                                    <div class="choice-options">
                                    </div>
                                </div>'''

new_multiple_choice_content = '''                                <div class="multiple-choice-section">
                                    <h6>Select Your Answer:</h6>
                                    <div class="choice-options">
                                        {% for choice in question.get_choices_list %}
                                        <div class="form-check">
                                            <input class="form-check-input" type="radio" 
                                                   name="question_{{ question.id }}" 
                                                   id="choice_{{ forloop.counter }}_{{ question.id }}"
                                                   value="{{ forloop.counter0 }}">
                                            <label class="form-check-label" for="choice_{{ forloop.counter }}_{{ question.id }}">
                                                {{ choice }}
                                            </label>
                                        </div>
                                        {% empty %}
                                        <div class="alert alert-info">
                                            <small>No multiple choice options available.</small>
                                        </div>
                                        {% endfor %}
                                    </div>
                                </div>'''

# Replace just the multiple choice content
content = content.replace(old_multiple_choice_content, new_multiple_choice_content)

with open('./study_app/templates/study_app/take_quiz.html', 'w') as f:
    f.write(content)

print("✓ Restored multiple choice answers while keeping all other sections")
