#!/bin/bash

echo "=== ADDING MISSING PHRASES TO PO FILE ==="
echo ""

PO_FILE="./locale/es/LC_MESSAGES/django.po"

# Create backup
cp "$PO_FILE" "${PO_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

# Add missing phrases using Python for proper handling
python3 -c "
import re
from pathlib import Path

po_file = Path('./locale/es/LC_MESSAGES/django.po')

missing_translations = {
    'Read Online': 'Leer en Línea',
    'Comprehensive study of the fundamental texts of Gaudiya Vaishnavism including Bhagavad-gita and essential scriptures.': 
        'Estudio completo de los textos fundamentales del Gaudiya Vaishnavismo incluyendo el Bhagavad-gita y las escrituras esenciales.',
    'Study Materials': 'Materiales de Estudio'
}

if po_file.exists():
    content = po_file.read_text(encoding='utf-8')
    
    for english, spanish in missing_translations.items():
        # Check if already exists
        if f'msgid \"{english}\"' not in content:
            # Add new entry at the end of the file, before the last line
            new_entry = f'\n#: Added manually\\nmsgid \"{english}\"\\nmsgstr \"{spanish}\"\\n'
            
            # Insert before the last line (which should be empty or the end)
            lines = content.split('\\n')
            if lines and lines[-1] == '':
                lines.insert(-1, new_entry.strip())
            else:
                lines.append(new_entry.strip())
            
            content = '\\n'.join(lines)
            print(f'✅ Added: {english}')
        else:
            print(f'⚠️  Already exists: {english}')
    
    po_file.write_text(content, encoding='utf-8')
    print('\\n🎉 Missing phrases added to PO file!')
else:
    print('❌ PO file not found')
"

echo ""
echo "🔨 Compiling messages..."
python3 manage.py compilemessages

echo ""
echo "🧪 Testing all translations..."
python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
import django
django.setup()

from django.utils.translation import activate, gettext as _

activate('es')
print('Testing ALL translations:')

test_phrases = [
    'Back to Courses',
    'Study This Book', 
    'Read Online',
    'Comprehensive study of the fundamental texts of Gaudiya Vaishnavism including Bhagavad-gita and essential scriptures.',
    'Read Online (English)',
    'Read Online (Spanish)', 
    'Study Tools',
    'Study Questions',
    'Study Materials'
]

for phrase in test_phrases:
    translated = _(phrase)
    if translated != phrase:
        print(f'✅ WORKING: {phrase} -> {translated}')
    else:
        print(f'❌ STILL NOT WORKING: {phrase}')
"
