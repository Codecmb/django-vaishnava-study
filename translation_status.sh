#!/bin/bash

echo "=== SPANISH TRANSLATION STATUS SUMMARY ==="
echo ""

# Check PO file status
PO_FILE="./locale/es/LC_MESSAGES/django.po"
if [[ -f "$PO_FILE" ]]; then
    echo "📊 PO File Status:"
    msgfmt --statistics "$PO_FILE" 2>&1
else
    echo "❌ No PO file found"
fi

echo ""
echo "🌐 URL Testing:"
echo "   English: http://localhost:8000/"
echo "   Spanish: http://localhost:8000/es/"

echo ""
echo "🔧 Next steps:"
echo "   1. Check if Spanish page shows translated text"
echo "   2. Add missing translations to the PO file"
echo "   3. Add {% trans %} tags to any untranslated template text"
echo "   4. Run: python3 manage.py compilemessages after changes"
echo "   5. Restart server to see changes"

echo ""
echo "📝 Quick commands:"
echo "   python3 manage.py makemessages -l es    # Update PO file"
echo "   python3 manage.py compilemessages       # Compile translations"
echo "   python3 manage.py runserver            # Test locally"
