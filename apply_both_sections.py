import re

with open('./study_app/templates/study_app/take_quiz.html', 'r') as f:
    content = f.read()

# Replace the old form field with new multiple choice, but keep AI section
old_pattern = r'<div class="multiple-choice-section">.*?{{ form\\|get_field:question\\.id }}.*?</div>\\s*<div class="ai-section">'

new_section = '''<div class="multiple-choice-section">
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
                                </div>
                                <div class="ai-section">'''

content = re.sub(old_pattern, new_section, content, flags=re.DOTALL)

with open('./study_app/templates/study_app/take_quiz.html', 'w') as f:
    f.write(content)

print("✓ Applied both multiple choice and AI section")
