#!/bin/bash

echo "=== FIXING 'STUDY THIS BOOK' TRANSLATION ==="
echo ""

PO_FILE="./locale/es/LC_MESSAGES/django.po"

# Find the current translation
echo "🔍 Current translation for 'Study This Book':"
grep -A 1 'msgid "Study This Book"' "$PO_FILE"

echo ""
echo "🔄 Updating translation to 'Estudie este Libro'..."
echo ""

# Create backup
cp "$PO_FILE" "${PO_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

# Update the translation
sed -i 's/msgid "Study This Book"/msgid "Study This Book"/' "$PO_FILE"
sed -i '/msgid "Study This Book"/{n;s/msgstr ".*"/msgstr "Estudie este Libro"/}' "$PO_FILE"

echo "✅ Translation updated:"
grep -A 1 'msgid "Study This Book"' "$PO_FILE"

echo ""
echo "🔨 Compiling messages..."
python3 manage.py compilemessages

echo ""
echo "🎉 Translation fixed! The Spanish version should now show 'Estudie este Libro'"
echo "🌐 Test at: http://localhost:8000/es/"
