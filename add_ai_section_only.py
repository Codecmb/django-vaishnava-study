with open('./study_app/templates/study_app/take_quiz.html', 'r') as f:
    content = f.read()

# The AI section to add (exactly as it was)
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

# Find the exact end of the multiple choice section and insert AI section after it
# Look for the closing div of multiple-choice-section
import re
pattern = r'(</div>\\s*<!-- multiple-choice-section end -->)'

if re.search(pattern, content):
    content = re.sub(pattern, r'\\1' + ai_section, content)
else:
    # If no comment, look for the closing div and next section
    pattern = r'(</div>\\s*</div>\\s*</div>\\s*{% endfor %)'
    content = re.sub(pattern, ai_section + r'\\1', content)

with open('./study_app/templates/study_app/take_quiz.html', 'w') as f:
    f.write(content)

print("✓ Added AI section with student input box - nothing removed")
