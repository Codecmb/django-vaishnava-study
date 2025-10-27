#!/usr/bin/env python3
"""
Fix the take_quiz.html template to restore submit button and fix layout
"""

def fix_template():
    with open('study_app/templates/study_app/take_quiz.html', 'r') as f:
        content = f.read()
    
    # Check if submit button exists
    if 'Submit Quiz' not in content:
        print("✗ Submit button is missing! Restoring it...")
        
        # Find where to add the submit button (should be after all questions)
        if '{% endfor %}' in content:
            # Add the submit button section after the question loop
            submit_section = '''
                        {% endfor %}
                        
                        <div class="text-center mt-4">
                            <button type="submit" class="btn btn-primary btn-lg">
                                {% trans "Submit Quiz" %}
                            </button>
                            <a href="{% url 'study_app:quiz_dashboard' book.id %}" class="btn btn-secondary btn-lg">
                                {% trans "Cancel" %}
                            </a>
                        </div>
                    </form>'''
            
            # Replace the end of the form
            if '{% endfor %}</form>' in content:
                content = content.replace('{% endfor %}</form>', submit_section)
            elif '{% endfor %}\n</form>' in content:
                content = content.replace('{% endfor %}\n</form>', submit_section)
            else:
                # Try to find the form end after the loop
                endfor_pos = content.find('{% endfor %}')
                form_end_pos = content.find('</form>', endfor_pos)
                if endfor_pos != -1 and form_end_pos != -1:
                    content = content[:endfor_pos] + submit_section + content[form_end_pos + 7:]
    
    # Also fix the textarea placeholder
    if 'Srila Prabhupada teachings...' in content:
        content = content.replace('Srila Prabhupada teachings...', 'Srila Prabhupada\\'s teachings...')
    
    # Write the fixed content
    with open('study_app/templates/study_app/take_quiz.html', 'w') as f:
        f.write(content)
    
    print("✓ Template fixed - submit button should be restored")

if __name__ == "__main__":
    fix_template()
