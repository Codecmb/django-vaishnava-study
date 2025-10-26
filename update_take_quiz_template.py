#!/usr/bin/env python3
import os

print("🔧 UPDATING TAKE QUIZ TEMPLATE FOR MULTIPLE CHOICE")
print("=" * 50)

take_quiz_file = 'study_app/templates/study_app/take_quiz.html'

if os.path.exists(take_quiz_file):
    with open(take_quiz_file, 'r') as f:
        content = f.read()
    
    # Check if it already handles multiple choice
    if 'multiple_choice_options' in content:
        print("✅ Template already has multiple choice support")
    else:
        print("❌ Template needs multiple choice support")
        
        # Create backup
        os.system(f'cp {take_quiz_file} {take_quiz_file}.backup')
        
        # Find where questions are displayed and add multiple choice
        if '{% for question in questions %}' in content:
            # Replace the question display section with multiple choice support
            multiple_choice_section = '''
{% for question in questions %}
<div class="card mb-4">
    <div class="card-header">
        <h5 class="mb-0">Question {{ forloop.counter }}</h5>
        {% if question.verse_reference %}
        <small class="text-muted">Reference: {{ question.verse_reference }}</small>
        {% endif %}
    </div>
    <div class="card-body">
        <p class="card-text"><strong>{{ question.question_text }}</strong></p>
        
        {% with question.get_multiple_choice_list as options %}
        {% if options %}
        <div class="multiple-choice-options">
            {% for option in options %}
            <div class="form-check">
                <input class="form-check-input" type="radio" 
                       name="question_{{ question.id }}" 
                       id="question_{{ question.id }}_{{ forloop.counter }}"
                       value="{{ option }}">
                <label class="form-check-label" for="question_{{ question.id }}_{{ forloop.counter }}">
                    {{ option }}
                </label>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="form-group">
            <label for="question_{{ question.id }}">Your Answer:</label>
            <textarea class="form-control" id="question_{{ question.id }}" 
                      name="question_{{ question.id }}" rows="3" 
                      placeholder="Enter your answer here..."></textarea>
        </div>
        {% endif %}
        {% endwith %}
    </div>
</div>
{% endfor %}
'''
            
            # Find and replace the question loop
            import re
            pattern = r'\{% for question in questions %\}.*?\{% endfor %\}'
            new_content = re.sub(pattern, multiple_choice_section, content, flags=re.DOTALL)
            
            with open(take_quiz_file, 'w') as f:
                f.write(new_content)
            print("✅ Updated take quiz template with multiple choice support!")
        else:
            print("❌ Could not find question loop in template")
else:
    print("❌ take_quiz.html not found")
