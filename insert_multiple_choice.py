with open('./study_app/templates/study_app/take_quiz.html', 'r') as f:
    content = f.read()

# Replace the placeholder with actual multiple choice code
placeholder = '       <!-- Multiple choice options should go here -->'
multiple_choice_code = '''       <div class="choice-options">
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

if placeholder in content:
    content = content.replace(placeholder, multiple_choice_code)
    print("✓ Successfully inserted multiple choice questions")
else:
    print("⚠️  Placeholder not found. Please insert manually using the guide.")

with open('./study_app/templates/study_app/take_quiz.html', 'w') as f:
    f.write(content)
