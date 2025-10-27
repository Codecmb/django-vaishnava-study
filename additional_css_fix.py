#!/usr/bin/env python3
"""
Additional CSS fixes for layout
"""

def css_fix():
    with open('study_app/templates/study_app/take_quiz.html', 'r') as f:
        content = f.read()
    
    # Add additional CSS for form controls
    additional_css = '''
.form-control {
    width: 100% !important;
    display: block !important;
}
.form-group {
    width: 100%;
}
.answer-section .form-label {
    display: block;
    width: 100%;
    margin-bottom: 8px;
}
'''
    
    # Insert before existing style closing tag
    style_end = content.find('</style>')
    if style_end != -1:
        content = content[:style_end] + additional_css + content[style_end:]
    
    with open('study_app/templates/study_app/take_quiz.html', 'w') as f:
        f.write(content)
    
    print("✓ Additional CSS fixes applied")

if __name__ == "__main__":
    css_fix()
