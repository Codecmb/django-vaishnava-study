#!/bin/bash

echo "=== CHECKING TEMPLATES FOR TRANSLATION TAGS ==="
echo ""

echo "📋 Templates that might need translation tags:"
find ./study_app/templates -name "*.html" | while read template; do
    # Check if template has text but no translation tags
    if grep -q "[A-Za-z]" "$template" && ! grep -q "{% trans" "$template"; then
        echo "→ $template (may need translation tags)"
        # Show some sample text
        grep -h -o "[A-Z][a-z ]*" "$template" | head -3 | while read line; do
            if [[ ${#line} -gt 5 && ${#line} -lt 50 ]]; then
                echo "  Sample: '$line'"
            fi
        done
    fi
done

echo ""
echo "🔧 To add translation tags, wrap text in templates like:"
echo "   {% trans \"Your English text here\" %}"
echo ""
echo "📝 Common places to check:"
echo "   - Page titles and headings"
echo "   - Navigation menu items"
echo "   - Button labels"
echo "   - Form labels and placeholders"
echo "   - Error/success messages"
