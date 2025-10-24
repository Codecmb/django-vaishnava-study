#!/bin/bash

echo "=== CHECKING BOOK-RELATED PHRASES ==="
echo ""

PO_FILE="./locale/es/LC_MESSAGES/django.po"

echo "📚 Book-related phrases in Spanish translations:"
echo ""

# Check various book-related phrases
phrases=(
    "Study This Book"
    "Read the Book" 
    "Books in this Course"
    "Back to Book"
    "About This Book"
    "Study Tools"
    "Study Questions"
)

for phrase in "${phrases[@]}"; do
    echo "🔍 '$phrase':"
    grep -A 1 "msgid \"$phrase\"" "$PO_FILE" 2>/dev/null || echo "   Not found or already translated"
    echo ""
done

echo "💡 If any translations need adjustment, we can fix them one by one."
