#!/bin/bash

echo "=== FINDING MISSING TRANSLATION TAGS IN TEMPLATES ==="
echo ""

echo "🔍 Checking templates for hard-coded English text that should be translatable..."
echo ""

TEMPLATE_DIR="./study_app/templates"

find "$TEMPLATE_DIR" -name "*.html" | while read template; do
    echo "📄 Checking: $template"
    
    # Look for common UI text that might not be translated
    COMMON_TERMS=("Home" "Courses" "Login" "Logout" "Save" "Delete" "Edit" "Submit" "Cancel" "Back" "Next")
    
    for term in "${COMMON_TERMS[@]}"; do
        if grep -q "$term" "$template" && ! grep -q "{% trans.*$term" "$template"; then
            echo "   ⚠️  '$term' found but may not be wrapped in {% trans %}"
        fi
    done
    
    # Count translation tags vs total text lines
    trans_count=$(grep -c "{% trans" "$template" 2>/dev/null || echo "0")
    if [ "$trans_count" -eq "0" ]; then
        echo "   ℹ️  No translation tags found in this template"
    else
        echo "   ✅ Found $trans_count translation tags"
    fi
done

echo ""
echo "💡 To fix missing translation tags:"
echo "   Replace: Home"
echo "   With: {% trans \"Home\" %}"
echo ""
echo "📝 Common templates to check:"
echo "   - base.html"
echo "   - includes/navbar.html" 
echo "   - index.html"
echo "   - course_detail.html"
echo "   - book_detail.html"
