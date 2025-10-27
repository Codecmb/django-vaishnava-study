#!/usr/bin/env python3
"""
Create integrated layout with multiple choice and AI features in same container
"""

def create_integrated_layout():
    with open('study_app/templates/study_app/take_quiz.html', 'r') as f:
        content = f.read()
    
    print("Creating integrated layout...")
    
    # 1. Add AI CSS styles
    style_end = content.find('</style>')
    if style_end != -1:
        ai_css = '''
/* AI Validation Styles - Integrated */
.ai-features-container {
    margin-top: 20px;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #17a2b8;
}

.written-answer-section {
    margin-bottom: 15px;
}

.written-answer-section label {
    font-weight: 600;
    color: #495057;
    margin-bottom: 8px;
    display: block;
}

.commentary-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 15px;
    margin-top: 15px;
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
    margin: 15px 0;
}

.btn-info {
    background-color: #17a2b8;
    border-color: #17a2b8;
    color: white;
}

/* Ensure good spacing */
.question-card .card-body {
    padding: 25px;
}
'''
        content = content[:style_end] + ai_css + content[style_end:]
        print("✓ Added integrated CSS styles")
    
    # 2. Update instructions
    if '💡' not in content:
        old_instructions = '''<p class="mb-0">
                            {% trans "Answer each question based on your understanding of Srila Prabhupada's commentaries. There are no 'wrong' answers - this is to help you gauge your philosophical understanding." %}
                        </p>'''
        new_instructions = '''<p class="mb-0">
                            {% trans "Answer each question based on your understanding of Srila Prabhupada's commentaries. There are no 'wrong' answers - this is to help you gauge your philosophical understanding." %}
                        </p>
                        <p class="mb-0 mt-2">
                            <small>💡 <strong>New AI Feature:</strong> Select multiple choice answers AND write detailed explanations for AI validation!</small>
                        </p>'''
        content = content.replace(old_instructions, new_instructions)
        print("✓ Updated instructions")
    
    # 3. Replace the question section - INTEGRATE multiple choice with AI features
    old_section = '''{{ form|get_field:question.id }}
                                
                                {% if question.prabhupada_commentary %}
                                <div class="mt-3 p-3 bg-light rounded">
                                    <small class="text-muted">
                                        <strong>{% trans "Srila Prabhupada's Commentary:" %}</strong><br>
                                        {{ question.prabhupada_commentary|truncatewords:30 }}
                                    </small>
                                </div>
                                {% endif %}'''
    
    new_section = '''<div class="multiple-choice-section">
                                    {{ form|get_field:question.id }}
                                </div>
                                
                                <!-- Integrated AI Features Container -->
                                <div class="ai-features-container">
                                    <div class="written-answer-section">
                                        <label for="written_answer_{{ question.id }}" class="form-label">
                                            <strong>💭 Your Detailed Understanding (Optional AI Analysis):</strong>
                                        </label>
                                        <textarea 
                                            id="written_answer_{{ question.id }}" 
                                            name="written_answer_{{ question.id }}" 
                                            rows="4" 
                                            class="form-control"
                                            placeholder="Elaborate on your answer based on Srila Prabhupada's teachings for AI analysis..."
                                        ></textarea>
                                    </div>
                                    
                                    <div class="validation-section">
                                        <button type="button" 
                                                onclick="validateAnswer({{ question.id }})" 
                                                class="btn btn-info">
                                            🔍 Check Siddhanta Alignment
                                        </button>
                                        <div id="feedback-{{ question.id }}" class="feedback-container mt-2"></div>
                                    </div>
                                    
                                    <div class="commentary-section">
                                        <div class="commentary-box">
                                            <h6 class="mb-2">📖 Srila Prabhupada's Commentary:</h6>
                                            <div id="commentary-{{ question.id }}" class="commentary-content">
                                                {% if question.prabhupada_commentary %}
                                                    {{ question.prabhupada_commentary|linebreaks }}
                                                {% else %}
                                                    <em class="text-muted" id="default-commentary-{{ question.id }}">
                                                        Write your answer above and click "Check Siddhanta Alignment" to see relevant commentary...
                                                    </em>
                                                {% endif %}
                                            </div>
                                        </div>
                                    </div>
                                </div>'''
    
    if old_section in content:
        content = content.replace(old_section, new_section)
        print("✓ Integrated multiple choice with AI features")
    else:
        print("✗ Could not find the section to replace")
        return False
    
    # 4. Add JavaScript for AI validation
    javascript = '''
<script>
// Auto-show commentary when user starts typing
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea[id^="written_answer_"]');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            const questionId = this.id.replace('written_answer_', '');
            const defaultCommentary = document.getElementById('default-commentary-' + questionId);
            if (defaultCommentary && this.value.trim().length > 0) {
                defaultCommentary.innerHTML = 'Writing detected! Click "Check Siddhanta Alignment" for detailed analysis...';
            }
        });
    });
});

// AI Validation Function
function validateAnswer(questionId) {
    const answerInput = document.getElementById('written_answer_' + questionId);
    const answerText = answerInput.value.trim();
    
    if (!answerText) {
        alert('Please write your detailed answer before validating.');
        return;
    }
    
    // Show loading state
    const feedbackDiv = document.getElementById('feedback-' + questionId);
    feedbackDiv.innerHTML = '<div class="loading">🔄 AI is analyzing your answer against Srila Prabhupada\'s teachings...</div>';
    
    // Update commentary area
    const commentaryDiv = document.getElementById('commentary-' + questionId);
    commentaryDiv.innerHTML = '<div class="loading">Loading relevant commentary from Srila Prabhupada...</div>';
    
    fetch('/question/' + questionId + '/validate/', {
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
        
        // Display AI feedback
        const alignedClass = data.is_aligned ? 'aligned' : 'not-aligned';
        const alignedText = data.is_aligned ? '✅ Yes' : '❌ Needs improvement';
        
        feedbackDiv.innerHTML = `
            <div class="ai-feedback ${alignedClass}">
                <h6>🤖 AI Siddhanta Analysis</h6>
                <p><strong>Alignment Score:</strong> ${data.score}/100</p>
                <p><strong>Feedback:</strong> ${data.feedback}</p>
                <p><strong>Siddhanta Aligned:</strong> ${alignedText}</p>
            </div>
        `;
        
        // Update Prabhupada commentary
        if (data.prabhupada_commentary) {
            commentaryDiv.innerHTML = data.prabhupada_commentary;
        } else {
            commentaryDiv.innerHTML = '<em class="text-muted">No specific commentary available for this answer.</em>';
        }
    })
    .catch(error => {
        feedbackDiv.innerHTML = '<div class="error">❌ Network error. Please try again.</div>';
        console.error('Error:', error);
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
    print("✓ Added JavaScript for AI validation")
    
    # Write the integrated template
    with open('study_app/templates/study_app/take_quiz.html', 'w') as f:
        f.write(content)
    
    print("✓ Integrated layout created successfully!")
    print("✓ Multiple choice answers preserved")
    print("✓ AI features integrated in same container")
    print("✓ Submit button maintained")
    return True

if __name__ == "__main__":
    create_integrated_layout()
