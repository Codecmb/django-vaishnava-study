#!/usr/bin/env python3
"""
Safely update the take_quiz.html template with AI validation features
"""

def update_template():
    with open('study_app/templates/study_app/take_quiz.html', 'r') as f:
        content = f.read()
    
    # First, let's add the CSS and JavaScript at the end of the content block
    if 'ai-feedback' not in content:
        # Find the end of the content block
        style_pos = content.find('</style>')
        if style_pos != -1:
            # Add our CSS after the existing style tag
            new_css = '''
/* AI Validation Styles */
.commentary-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 15px;
    margin-top: 10px;
}

.commentary-box h6 {
    color: #856404;
    margin-bottom: 10px;
    font-weight: bold;
}

.commentary-content {
    color: #333;
    line-height: 1.5;
    font-size: 0.95em;
}

.ai-feedback {
    padding: 15px;
    margin: 10px 0;
    border-radius: 5px;
    border: 1px solid #ddd;
}

.ai-feedback.aligned {
    background-color: #e8f5e8;
    border-left: 4px solid #4CAF50;
}

.ai-feedback.not-aligned {
    background-color: #ffebee;
    border-left: 4px solid #f44336;
}

.loading {
    padding: 10px;
    background-color: #e3f2fd;
    border-left: 4px solid #2196F3;
    color: #0d47a1;
    border-radius: 5px;
}

.error {
    padding: 10px;
    background-color: #ffebee;
    border-left: 4px solid #f44336;
    color: #c62828;
    border-radius: 5px;
}

.validation-section {
    margin: 10px 0;
}
'''
            content = content[:style_pos + 8] + new_css + content[style_pos + 8:]
    
    # Now update the question section to add AI validation
    if 'Check Siddhanta Alignment' not in content:
        # Find the question section and replace the form field part
        old_section = '''{{ form|get_field:question.id }}
                                
                                {% if question.prabhupada_commentary %}
                                <div class="mt-3 p-3 bg-light rounded">
                                    <small class="text-muted">
                                        <strong>{% trans "Srila Prabhupada's Commentary:" %}</strong><br>
                                        {{ question.prabhupada_commentary|truncatewords:30 }}
                                    </small>
                                </div>
                                {% endif %}'''
        
        new_section = '''<!-- Student Answer Input -->
                                <div class="answer-section mb-3">
                                    <label for="answer_{{ question.id }}" class="form-label">
                                        <strong>{% trans "Share your understanding based on Srila Prabhupada's teachings:" %}</strong>
                                    </label>
                                    <textarea 
                                        id="answer_{{ question.id }}" 
                                        name="answer_{{ question.id }}" 
                                        rows="4" 
                                        class="form-control"
                                        placeholder="{% trans 'Share your understanding based on Srila Prabhupada teachings...' %}"
                                    ></textarea>
                                </div>
                                
                                <!-- AI Validation Button -->
                                <div class="validation-section mb-3">
                                    <button type="button" 
                                            onclick="validateAnswer({{ question.id }})" 
                                            class="btn btn-info btn-sm">
                                        🔍 {% trans "Check Siddhanta Alignment" %}
                                    </button>
                                    <div id="feedback-{{ question.id }}" class="feedback-container mt-2"></div>
                                </div>
                                
                                <!-- Srila Prabhupada Commentary Box -->
                                <div class="commentary-section">
                                    <div class="commentary-box">
                                        <h6>📖 {% trans "Srila Prabhupada's Commentary:" %}</h6>
                                        <div id="commentary-{{ question.id }}" class="commentary-content">
                                            {% if question.prabhupada_commentary %}
                                                {{ question.prabhupada_commentary|linebreaks }}
                                            {% else %}
                                                <em class="text-muted">{% trans "Relevant commentary from Srila Prabhupada will be displayed here after you validate your answer..." %}</em>
                                            {% endif %}
                                        </div>
                                    </div>
                                </div>'''
        
        if old_section in content:
            content = content.replace(old_section, new_section)
            print("✓ Updated question section with AI validation")
        else:
            print("✗ Could not find the exact section to replace")
    
    # Add JavaScript at the end
    if 'function validateAnswer' not in content:
        javascript = '''
<script>
// AI Validation Function
function validateAnswer(questionId) {
    const answerInput = document.getElementById(`answer_${questionId}`);
    const answerText = answerInput.value.trim();
    
    if (!answerText) {
        alert('{% trans "Please enter your answer before validating." %}');
        return;
    }
    
    // Show loading state
    const feedbackDiv = document.getElementById(`feedback-${questionId}`);
    feedbackDiv.innerHTML = '<div class="loading">🔄 {% trans "Analyzing with AI..." %}</div>';
    
    fetch(`/question/${questionId}/validate/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            answer: answerText
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            feedbackDiv.innerHTML = `<div class="error">❌ ${data.error}</div>`;
            return;
        }
        
        feedbackDiv.innerHTML = `
            <div class="ai-feedback ${data.is_aligned ? 'aligned' : 'not-aligned'}">
                <h6>🤖 {% trans "AI Analysis" %}</h6>
                <p><strong>{% trans "Score:" %}</strong> ${data.score}/100</p>
                <p><strong>{% trans "Feedback:" %}</strong> ${data.feedback}</p>
                <p><strong>{% trans "Siddhanta Aligned:" %}</strong> ${data.is_aligned ? '✅ {% trans "Yes" %}' : '❌ {% trans "Needs improvement" %}'}</p>
            </div>
        `;
    })
    .catch(error => {
        feedbackDiv.innerHTML = `<div class="error">❌ {% trans "Network error" %}</div>`;
    });
}

// CSRF token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
</script>
'''
        # Add JavaScript before the end of the content block
        content = content.replace('{% endblock %}', javascript + '\\n{% endblock %}')
        print("✓ Added JavaScript for AI validation")
    
    # Write the updated content
    with open('study_app/templates/study_app/take_quiz.html', 'w') as f:
        f.write(content)
    
    print("✓ Template updated successfully")

if __name__ == "__main__":
    update_template()
