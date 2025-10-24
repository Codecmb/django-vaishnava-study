#!/bin/bash

echo "=== FIXING HARDCODED TEXT IN TEMPLATES ==="
echo ""

# Fix templates with hardcoded text
declare -A fixes=(
    ["Back to Courses"]="Back to Courses"
    ["Study This Book"]="Study This Book"
    ["Read Online"]="Read Online"
    ["Study Tools"]="Study Tools"
    ["Study Questions"]="Study Questions"
    ["Study Materials"]="Study Materials"
)

for english in "${!fixes[@]}"; do
    echo "🔧 Fixing: $english"
    
    # Find files containing this hardcoded text
    find ./study_app/templates -name "*.html" -exec grep -l "$english" {} \; 2>/dev/null | while read file; do
        # Skip if already has translation tag
        if ! grep -q "{% trans.*$english.*%}" "$file" && ! grep -q "{% blocktranslate.*%}.*$english.*{% endblocktranslate %}" "$file"; then
            echo "   📄 Updating: $file"
            
            # Create backup
            cp "$file" "${file}.backup.$(date +%Y%m%d_%H%M%S)"
            
            # Replace hardcoded text with translation tag
            # Be careful with replacements to avoid breaking HTML
            sed -i "s/>$english</>{% trans \"$english\" %}</g" "$file"
            sed -i "s/\"$english\"/{% trans \"$english\" %}/g" "$file"
            sed -i "s/'$english'/{% trans \"$english\" %}/g" "$file"
            
            echo "   ✅ Fixed: $file"
        else
            echo "   ✅ Already has translation tag: $file"
        fi
    done
    echo ""
done

echo "🔄 Updating PO file with new translatable strings..."
python3 manage.py makemessages -l es -i "venv/*"

echo ""
echo "🔨 Compiling messages..."
python3 manage.py compilemessages

echo ""
echo "🎉 Templates updated and translations compiled!"
