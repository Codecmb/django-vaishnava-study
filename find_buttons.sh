#!/bin/bash

echo "=== SEARCHING FOR BUTTONS IN TEMPLATES ==="

# Find all HTML files containing buttons
echo "Files containing 'button':"
find ./study_app/templates -name "*.html" -exec grep -l "button" {} \; | while read file; do
    echo "→ $file"
    grep -n "button" "$file" | head -5
done

echo ""
echo "Files containing 'Explorar':"
find ./study_app/templates -name "*.html" -exec grep -l "Explorar" {} \; | while read file; do
    echo "→ $file"
    grep -n "Explorar" "$file"
done

echo ""
echo "Files containing 'Bhakti Shastri':"
find ./study_app/templates -name "*.html" -exec grep -l "Bhakti Shastri" {} \; | while read file; do
    echo "→ $file"
    grep -n "Bhakti Shastri" "$file" | head -3
done

echo ""
echo "=== CURRENT INDEX.HTML CONTENT (first 60 lines) ==="
head -60 ./study_app/templates/study_app/index.html
