#!/bin/bash

echo "=== CHECKING PO FILE CONTENTS ==="
echo ""

PO_FILE="./locale/es/LC_MESSAGES/django.po"

echo "🔍 Checking if our translations exist in PO file..."
echo ""

phrases_to_check=(
    "Back to Courses"
    "Study This Book"
    "Read Online"
    "Comprehensive study of the fundamental texts of Gaudiya Vaishnavism including Bhagavad-gita and essential scriptures."
    "Read Online (English)"
    "Read Online (Spanish)"
    "Study Tools"
    "Study Questions"
    "Study Materials"
)

for phrase in "${phrases_to_check[@]}"; do
    if grep -q "msgid \"$phrase\"" "$PO_FILE"; then
        echo "✅ Found in PO: $phrase"
        grep -A 1 "msgid \"$phrase\"" "$PO_FILE"
    else
        echo "❌ NOT in PO: $phrase"
    fi
    echo ""
done

echo "💡 Missing phrases need to be added to PO file using makemessages"
