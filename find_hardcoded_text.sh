#!/bin/bash

echo "=== FINDING HARDCODED TEXT IN TEMPLATES ==="
echo ""

echo "🔍 Searching for hardcoded text that needs translation tags..."
echo ""

# Check for our specific phrases in templates
phrases=(
    "Back to Courses"
    "Study This Book"
    "Read Online"
    "Comprehensive study of the fundamental texts"
    "Study Tools"
    "Study Questions"
    "Study Materials"
)

for phrase in "${phrases[@]}"; do
    echo "📖 Searching for: '$phrase'"
    find ./study_app/templates -name "*.html" -exec grep -l "$phrase" {} \; 2>/dev/null | while read file; do
        echo "   📄 File: $file"
        # Check if it has translation tags
        if grep -q "{% trans.*$phrase.*%}" "$file" || grep -q "{% blocktranslate.*%}.*$phrase.*{% endblocktranslate %}" "$file"; then
            echo "   ✅ Has translation tag"
        else
            echo "   ❌ HARDCODED - needs translation tag"
            # Show the context
            grep -n -B 2 -A 2 "$phrase" "$file" | head -10
        fi
        echo "   ---"
    done
    echo ""
done

echo "💡 We need to wrap hardcoded text in {% trans %} tags"
