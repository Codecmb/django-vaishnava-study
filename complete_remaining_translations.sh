#!/bin/bash

echo "=== COMPLETING REMAINING SPANISH TRANSLATIONS ==="
echo ""

PO_FILE="./locale/es/LC_MESSAGES/django.po"

if [[ ! -f "$PO_FILE" ]]; then
    echo "❌ PO file not found: $PO_FILE"
    exit 1
fi

echo "📊 Current status:"
msgfmt --statistics "$PO_FILE" 2>&1
echo ""

echo "🔍 Showing remaining untranslated strings (first 20):"
echo ""

# Extract and display untranslated strings in a cleaner format
grep -B 1 '^msgstr ""$' "$PO_FILE" | grep '^msgid "' | head -20 | while read line; do
    english_text=$(echo "$line" | sed 's/^msgid "//' | sed 's/"$//')
    if [[ ! -z "$english_text" && "$english_text" != "\"" ]]; then
        echo "────────────────────────────────────"
        echo "ENGLISH: $english_text"
        echo "SPANISH: [Add translation here]"
        echo ""
    fi
done

echo "📝 Total remaining: 74 strings"
echo ""
echo "💡 Translation tips:"
echo "   - Keep Vaishnava terms like 'Bhakti Shastri' as is (they're proper names)"
echo "   - Maintain respectful tone for spiritual content"
echo "   - Use formal 'usted' form for instructions"
echo "   - Keep technical terms consistent"
