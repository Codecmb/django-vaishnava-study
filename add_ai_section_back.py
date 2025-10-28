import re

with open('./study_app/templates/study_app/take_quiz.html', 'r') as f:
    content = f.read()

# Find where the multiple choice section ends and add AI section after it
ai_section = '''
                                <div class="ai-section">
                                    <h6>AI Learning Features</h6>
                                    
                                    <div class="written-answer-box">
                                        <label>Write Your Understanding:</label>
                                        <textarea 
                                            id="written_answer_{{ question.id }}" 
                                            placeholder="Share your thoughts based on Srila Prabhupada's teachings..."
                                        ></textarea>
                                    </div>
                                    
                                    <div class="validation-area">
                                        <button type="button" 
                                                onclick="validateAnswer({{ question.id }})" 
                                                class="btn-validate">
                                            Check Siddhanta Alignment
                                        </button>
                                        <div id="feedback-{{ question.id }}" class="mt-3"></div>
                                    </div>
                                    
                                    <div class="commentary-box">
                                        <h6>Srila Prabhupada's Commentary</h6>
                                        <div id="commentary-{{ question.id }}">
                                            {% if question.prabhupada_commentary %}
                                                {{ question.prabhupada_commentary|linebreaks }}
                                            {% else %}
                                                <em>Write your answer and click validate to see commentary</em>
                                            {% endif %}
                                        </div>
                                    </div>
                                </div>'''

# Insert AI section after the multiple choice section
content = re.sub(
    r'(</div>\\s*</div>\\s*<!-- End multiple choice section -->)',
    r'\\1' + ai_section,
    content
)

# If the comment isn't there, just add after the multiple choice div
if '<!-- End multiple choice section -->' not in content:
    content = re.sub(
        r'(</div>\\s*</div>\\s*)(?=\\s*{% endfor %})',
        r'\\1' + ai_section,
        content
    )

with open('./study_app/templates/study_app/take_quiz.html', 'w') as f:
    f.write(content)

print("✓ Added AI section with student input box back")
