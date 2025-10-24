#!/bin/bash

echo "=== TESTING ALL UPDATED TRANSLATIONS ==="
echo ""

echo "🧪 Testing translations in Django:"
python3 -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
import django
django.setup()

from django.utils.translation import activate, gettext as _

activate('es')
print('Testing updated translations:')

test_phrases = {
    'Back to Courses': 'Regresar al Curso',
    'Study This Book': 'Estudiar este Libro',
    'Read Online': 'Leer en Línea',
    'Comprehensive study of the fundamental texts of Gaudiya Vaishnavism including Bhagavad-gita and essential scriptures.': 
        'Estudio completo de los textos fundamentales del Gaudiya Vaishnavismo incluyendo el Bhagavad-gita y las escrituras esenciales.',
    'Back to Course': 'Regresar al Curso',
    'Read Online (English)': 'Leer en Línea (Inglés)',
    'Read Online (Spanish)': 'Leer en Línea (Español)',
    'Study Tools': 'Herramientas de Estudio',
    'Study Questions': 'Preguntas de Estudio',
    'Take Quiz': 'Realizar Examen',
    'Questions & Answers': 'Preguntas y Respuestas',
    'Study Materials': 'Materiales de Estudio',
    'Available Courses': 'Cursos Disponibles',
    'Explore Course': 'Explorar Curso'
}

for english, expected_spanish in test_phrases.items():
    try:
        translated = _(english)
        status = '✅' if translated == expected_spanish else '❌'
        print(f'{status} {english}')
        print(f'     Got: {translated}')
        if translated != expected_spanish:
            print(f'     Expected: {expected_spanish}')
    except Exception as e:
        print(f'❌ {english} -> Error: {e}')
"

echo ""
echo "🚀 Starting server for manual testing..."
python3 manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
SERVER_PID=$!

sleep 3

echo "🌐 Quick web test..."
if curl -s http://localhost:8000/es/ | grep -q "Estudiar este Libro"; then
    echo "✅ 'Estudiar este Libro' found on Spanish homepage"
else
    echo "❌ 'Estudiar este Libro' not found - may be in course pages only"
fi

kill $SERVER_PID 2>/dev/null

echo ""
echo "📝 Manual testing instructions:"
echo "   1. python3 manage.py runserver"
echo "   2. Visit: http://localhost:8000/es/"
echo "   3. Click on 'Cursos Disponibles'"
echo "   4. Click on 'Bhakti Shastri' course"
echo "   5. Verify all four books show:"
echo "      - 'Estudiar este Libro'"
echo "      - 'Leer en Línea' buttons"
echo "      - 'Regresar al Curso' link"
echo "   6. Check course description contains proper Spanish text"
