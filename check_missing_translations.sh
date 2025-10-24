#!/bin/bash

echo "=== MISSING SPANISH TRANSLATIONS ==="
echo ""

PO_FILE="./locale/es/LC_MESSAGES/django.po"

if [[ ! -f "$PO_FILE" ]]; then
    echo "❌ PO file not found: $PO_FILE"
    exit 1
fi

echo "📋 Untranslated strings (first 30):"
echo ""

# Use a simpler approach to find untranslated strings
grep -B 1 '^msgstr ""$' "$PO_FILE" | grep '^msgid "' | head -30 | while read line; do
    english_text=$(echo "$line" | sed 's/^msgid "//' | sed 's/"$//')
    if [[ ! -z "$english_text" ]]; then
        echo "English: $english_text"
        echo "Spanish: "
        echo "---"
    fi
done

echo ""
echo "📊 Total untranslated: $(grep -c '^msgstr ""$' "$PO_FILE")"
echo ""
echo "📝 To add translations, edit: $PO_FILE"
echo "   Look for 'msgstr \"\"' lines and add Spanish text between the quotes"
