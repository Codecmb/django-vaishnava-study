#!/usr/bin/env python3
"""
Targeted fix for the submit button
"""

def fix_submit():
    with open('study_app/templates/study_app/take_quiz.html', 'r') as f:
        content = f.read()
    
    # Check if the submit button section exists
    if 'Submit Quiz' not in content:
        print("Submit button missing! Adding it...")
        
        # Find the end of the form and add submit button before closing form tag
        form_end = content.find('</form>')
        if form_end != -1:
            submit_section = '''
                        <div class="text-center mt-4">
                            <button type="submit" class="btn btn-primary btn-lg">
                                Submit Quiz
                            </button>
                            <a href="{% url \\\"study_app:quiz_dashboard\\\" book.id %}" class="btn btn-secondary btn-lg">
                                Cancel
                            </a>
                        </div>
                    </form>'''
            content = content[:form_end] + submit_section
            print("✓ Submit button added")
        else:
            print("✗ Could not find form end")
    else:
        print("✓ Submit button already exists")
    
    # Write the fixed content
    with open('study_app/templates/study_app/take_quiz.html', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    fix_submit()
