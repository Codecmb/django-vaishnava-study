#!/usr/bin/env python3
"""
Final fix with proper template syntax for website.settings
"""

def final_fix():
    # Read the original backup
    with open('study_app/templates/study_app/take_quiz.html.backup', 'r') as f:
        content = f.read()
    
    # 1. Add AI CSS styles
    style_end = content.find('</style>')
    if style_end != -1:
        ai_css = '''
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

.answer-section {
    margin: 15px 0;
}
'''
        content = content[:style_end] + ai_css + content[style_end:]
    
    # 2. Update instructions (keep original trans tags)
    if '💡' not in content:
        old_instructions = '''<p class="mb-0">
                            {% trans "Answer each question based on your understanding of Srila Prabhupada's commentaries. There are no 'wrong' answers - this is to help you gauge your philosophical understanding." %}
                        </p>'''
        new_instructions = '''<p class="mb-0">
                            {% trans "Answer each question based on your understanding of Srila Prabhupada's commentaries. There are no 'wrong' answers - this is to help you gauge your philosophical understanding." %}
                        </p>
                        <p class="mb-0 mt-2">
                            <small>💡 <strong>New:</strong> Use the "Check Siddhanta Alignment" button to get AI feedback on your answers!</small>
                        </p>'''
        content = content.replace(old_instructions, new_instructions)
    
    # 3. Replace the question section - use simple text to avoid trans issues
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
                                        <strong>Share your understanding based on Srila Prabhupada's teachings:</strong>
                                    </label>
                                    <textarea 
                                        id="answer_{{ question.id }}" 
                                        name="answer_{{ question.id }}" 
                                        rows="4" 
                                        class="form-control"
                                        placeholder="Share your understanding based on Srila Prabhupada's teachings..."
                                    ></textarea>
                                </div>
                                
                                <!-- AI Validation Button -->
                                <div class="validation-section mb-3">
                                    <button type="button" 
                                            onclick="validateAnswer({{ question.id }})" 
                                            class="btn btn-info btn-sm">
                                        🔍 Check Siddhanta Alignment
                                    </button>
                                    <div id="feedback-{{ question.id }}" class="feedback-container mt-2"></div>
                                </div>
                                
                                <!-- Srila Prabhupada Commentary Box -->
                                <div class="commentary-section">
                                    <div class="commentary-box">
                                        <h6>📖 Srila Prabhupada's Commentary:</h6>
                                        <div id="commentary-{{ question.id }}" class="commentary-content">
                                            {% if question.prabhupada_commentary %}
                                                {{ question.prabhupada_commentary|linebreaks }}
                                            {% else %}
                                                <em class="text-muted">Relevant commentary from Srila Prabhupada will be displayed here after you validate your answer...</em>
                                            {% endif %}
                                        </div>
                                    </div>
                                </div>'''
    
    content = content.replace(old_section, new_section)
    
    # 4. Add JavaScript (use simple text to avoid template issues)
    javascript = '''
<script>
// AI Validation Function
function validateAnswer(questionId) {
    const answerInput = document.getElementById(`answer_${questionId}`);
    const answerText = answerInput.value.trim();
    
    if (!answerText) {
        alert('Please enter your answer before validating.');
        return;
    }
    
    // Show loading state
    const feedbackDiv = document.getElementById(`feedback-${questionId}`);
    feedbackDiv.innerHTML = '<div class="loading">🔄 Analyzing with AI...</div>';
    
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
            feedbackDiv.innerHTML = '<div class="error">❌ ' + data.error + '</div>';
            return;
        }
        
        const alignedClass = data.is_aligned ? 'aligned' : 'not-aligned';
        const alignedText = data.is_aligned ? '✅ Yes' : '❌ Needs improvement';
        
        feedbackDiv.innerHTML = `
            <div class="ai-feedback ${alignedClass}">
                <h6>🤖 AI Analysis</h6>
                <p><strong>Score:</strong> ${data.score}/100</p>
                <p><strong>Feedback:</strong> ${data.feedback}</p>
                <p><strong>Siddhanta Aligned:</strong> ${alignedText}</p>
            </div>
        `;
    })
    .catch(error => {
        feedbackDiv.innerHTML = '<div class="error">❌ Network error</div>';
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
    content = content.replace('{% endblock %}', javascript + '\\n{% endblock %}')
    
    # Write the final content
    with open('study_app/templates/study_app/take_quiz.html', 'w') as f:
        f.write(content)
    
    print("✓ Final template created successfully")

if __name__ == "__main__":
    final_fix()
