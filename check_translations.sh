#!/bin/bash

echo "=== CURRENT TRANSLATION STATUS ==="
echo ""

# Check if locale directory exists
if [[ ! -d "./locale" ]]; then
    echo "❌ No locale directory found. Creating basic structure..."
    mkdir -p ./locale/es/LC_MESSAGES
fi

# Check for PO files
echo "📁 PO Files found:"
find ./locale -name "*.po" -type f

echo ""
echo "🔍 Checking translation completeness:"

for po_file in $(find ./locale -name "*.po"); do
    echo ""
    echo "→ $po_file"
    if command -v msgfmt &> /dev/null; then
        msgfmt --statistics "$po_file" 2>&1
    else
        echo "❌ msgfmt not found. Install gettext: sudo apt-get install gettext"
    fi
done

echo ""
echo "🚀 Quick translation commands:"
echo "python3 manage.py makemessages -l es -i 'venv/*'  # Update PO files"
echo "python3 manage.py compilemessages                 # Compile translations"
echo "python3 manage.py runserver                       # Test Spanish at /es/"
