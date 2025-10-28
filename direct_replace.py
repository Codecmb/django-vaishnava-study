with open('./study_app/templates/study_app/take_quiz.html', 'r') as f:
    content = f.read()

# Replace the form field with multiple choice options
old_line = '                                    {{ form|get_field:question.id }}'

new_code = '''                                    <div class="choice-options">
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
                                    </div>'''

content = content.replace(old_line, new_code)

with open('./study_app/templates/study_app/take_quiz.html', 'w') as f:
    f.write(content)

print("✓ Directly replaced form field with multiple choice options")
