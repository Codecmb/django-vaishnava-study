#!/bin/bash

echo "=== SPANISH TRANSLATION WORKFLOW ==="
echo ""

while true; do
    echo ""
    echo "Choose an option:"
    echo "1. Check current translation status"
    echo "2. Show untranslated strings"
    echo "3. Update PO file with new strings"
    echo "4. Compile translations"
    echo "5. Test Spanish version"
    echo "6. Exit"
    echo ""
    read -p "Enter choice (1-6): " choice
    
    case $choice in
        1)
            echo ""
            echo "📊 Current status:"
            msgfmt --statistics "./locale/es/LC_MESSAGES/django.po" 2>&1
            ;;
        2)
            echo ""
            echo "🔍 Untranslated strings (first 15):"
            grep -B 1 '^msgstr ""$' "./locale/es/LC_MESSAGES/django.po" | grep '^msgid "' | head -15
            ;;
        3)
            echo ""
            echo "🔄 Updating PO file..."
            python3 manage.py makemessages -l es -i "venv/*"
            echo "✅ PO file updated"
            ;;
        4)
            echo ""
            echo "🔨 Compiling translations..."
            python3 manage.py compilemessages
            echo "✅ Translations compiled"
            ;;
        5)
            echo ""
            echo "🌐 Starting test server..."
            python3 manage.py runserver &
            SERVER_PID=$!
            echo "Server started (PID: $SERVER_PID)"
            echo "Test at: http://localhost:8000/es/"
            echo "Press Ctrl+C to stop server"
            wait $SERVER_PID
            ;;
        6)
            echo "¡Hasta luego! 👋"
            break
            ;;
        *)
            echo "Invalid choice"
            ;;
    esac
done
