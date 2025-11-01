#!/bin/bash
echo "=== TESTING STUDENT INPUT BOX ==="

echo "1. Checking take_quiz.html for student textarea..."
if grep -q 'textarea.*name="question_' study_app/templates/study_app/take_quiz.html; then
    echo "✅ SUCCESS: Student input textarea found!"
    echo "   Found these textarea elements:"
    grep -o 'name="question_[^"]*"' study_app/templates/study_app/take_quiz.html
else
    echo "❌ FAILED: No student input textarea found"
fi

echo ""
echo "2. Checking for multiple choice preservation..."
if grep -q "multiple_choice_options" study_app/templates/study_app/take_quiz.html; then
    echo "✅ SUCCESS: Multiple choice options preserved"
else
    echo "❌ FAILED: Multiple choice options missing"
fi

echo ""
echo "3. Checking form structure..."
echo "   - Form uses POST method: $(grep -q 'method="post"' study_app/templates/study_app/take_quiz.html && echo "✅" || echo "❌")"
echo "   - CSRF token present: $(grep -q 'csrf_token' study_app/templates/study_app/take_quiz.html && echo "✅" || echo "❌")"
echo "   - Textarea has rows=4: $(grep -q 'rows="4"' study_app/templates/study_app/take_quiz.html && echo "✅" || echo "❌")"

echo ""
echo "4. Template preview (first 15 lines):"
echo "-------------------------------------"
head -15 study_app/templates/study_app/take_quiz.html
echo "-------------------------------------"

echo ""
echo "=== TEST COMPLETE ==="
echo "If you see '✅ SUCCESS: Student input textarea found!' then the input box is restored."
