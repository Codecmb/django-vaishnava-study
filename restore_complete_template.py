#!/usr/bin/env python3
"""
Restore complete template with multiple choice, AI validation, and commentary
"""

def restore_complete():
    # Read the original backup
    with open('study_app/templates/study_app/take_quiz.html.backup', 'r') as f:
        content = f.read()
    
    print("Original template restored. Adding AI features...")
    
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

.written-answer-section {
    margin: 20px 0;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 5px;
    border-left: 4px solid #17a2b8;
}

.btn-info {
    background-color: #17a2b8;
    border-color: #17a2b8;
    color: white;
}
'''
        content = content[:style_end] + ai_css + content[style_end:]
        print("✓ Added AI CSS styles")
    
    # 2. Update instructions to mention AI feature
    if '💡' not in content:
        old_instructions = '''<p class="mb-0">
                            {% trans "Answer each question based on your understanding of Srila Prabhupada's commentaries. There are no 'wrong' answers - this is to help you gauge your philosophical understanding." %}
                        </p>'''
        new_instructions = '''<p class="mb-0">
                            {% trans "Answer each question based on your understanding of Srila Prabhupada's commentaries. There are no 'wrong' answers - this is to help you gauge your philosophical understanding." %}
                        </p>
                        <p class="mb-0 mt-2">
                            <small>💡 <strong>New AI Feature:</strong> After selecting multiple choice, write a detailed answer and use "Check Siddhanta Alignment" for AI feedback!</small>
                        </p>'''
        content = content.replace(old_instructions, new_instructions)
        print("✓ Updated instructions")
    
    # 3. Replace the question section - KEEP original multiple choice and ADD AI features
    old_section = '''{{ form|get_field:question.id }}
                                
                                {% if question.prabhupada_commentary %}
                                <div class="mt-3 p-3 bg-light rounded">
                                    <small class="text-muted">
                                        <strong>{% trans "Srila Prabhupada's Commentary:" %}</strong><br>
                                        {{ question.prabhupada_commentary|truncatewords:30 }}
                                    </small>
                                </div>
                                {% endif %}'''
    
    new_section = '''{{ form|get_field:question.id }}
                                
                                <!-- AI Validation Section -->
                                <div class="written-answer-section">
                                    <h6>💭 Optional Detailed Answer (for AI Analysis):</h6>
                                    <div class="form-group mt-2">
                                        <textarea 
                                            id="written_answer_{{ question.id }}" 
                                            name="written_answer_{{ question.id }}" 
                                            rows="4" 
                                            class="form-control"
                                            placeholder="Write your detailed understanding here for AI validation..."
                                            style="width: 100%;"
                                        ></textarea>
                                    </div>
                                    
                                    <!-- AI Validation Button -->
                                    <div class="validation-section">
                                        <button type="button" 
                                                onclick="validateAnswer({{ question.id }})" 
                                                class="btn btn-info btn-sm">
                                            🔍 Check Siddhanta Alignment
                                        </button>
                                        <div id="feedback-{{ question.id }}" class="feedback-container mt-2"></div>
                                    </div>
                                    
                                    <!-- Srila Prabhupada Commentary Box -->
                                    <div class="commentary-section mt-3">
                                        <div class="commentary-box">
                                            <h6>📖 Srila Prabhupada's Commentary:</h6>
                                            <div id="commentary-{{ question.id }}" class="commentary-content">
                                                {% if question.prabhupada_commentary %}
                                                    {{ question.prabhupada_commentary|linebreaks }}
                                                {% else %}
                                                    <em class="text-muted" id="default-commentary-{{ question.id }}">
                                                        Commentary will appear here when you use AI validation...
                                                    </em>
                                                {% endif %}
                                            </div>
                                        </div>
                                    </div>
                                </div>'''
    
    if old_section in content:
        content = content.replace(old_section, new_section)
        print("✓ Added AI validation section with multiple choice preserved")
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
                defaultCommentary.innerHTML = 'Continue writing and click "Check Siddhanta Alignment" for detailed commentary...';
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
    
    # Write the complete template
    with open('study_app/templates/study_app/take_quiz.html', 'w') as f:
        f.write(content)
    
    print("✓ Complete template restored with all features!")
    return True

if __name__ == "__main__":
    restore_complete()
