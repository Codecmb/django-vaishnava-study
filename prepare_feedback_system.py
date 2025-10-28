with open('./study_app/templates/study_app/take_quiz.html', 'r') as f:
    content = f.read()

# Add JavaScript to handle quiz submission and populate feedback
js_code = '''
<script>
// This will be called when we implement the feedback system
function populateFeedback(questionId, mcScore, writtenScore, feedbackText, commentary) {
    const feedbackBox = document.getElementById('system_feedback_' + questionId);
    const commentaryBox = document.getElementById('commentary_' + questionId);
    
    // Populate feedback box
    feedbackBox.value = `Multiple Choice: ${mcScore}/100\\nWritten Answer: ${writtenScore}/100\\n\\n${feedbackText}`;
    
    // Populate commentary
    if (commentary) {
        commentaryBox.innerHTML = commentary;
    }
}

// For demo purposes - this would be called after form submission
// In production, this would be populated from server response
document.addEventListener('DOMContentLoaded', function() {
    // This is where the feedback would be populated after quiz submission
    console.log('Feedback system ready - will populate after submission');
});
</script>
'''

# Insert JavaScript
if '<script>' in content:
    first_script = content.find('<script>')
    content = content[:first_script] + js_code + content[first_script:]
else:
    content = content.replace('</body>', js_code + '</body>')

with open('./study_app/templates/study_app/take_quiz.html', 'w') as f:
    f.write(content)

print("✓ Prepared feedback system for future implementation")
