#!/bin/bash

echo "=== FIXING REQUESTED TRANSLATIONS ==="
echo ""

PO_FILE="./locale/es/LC_MESSAGES/django.po"

# Create backup
cp "$PO_FILE" "${PO_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

echo "🔧 Fixing translations..."
echo ""

# Fix each requested translation
declare -A fixes=(
    # Your specific requests
    ["Back to Courses"]="Regresar al Curso"
    ["Study This Book"]="Estudiar este Libro"
    ["Read Online"]="Leer en Línea"
    ["Comprehensive study of the fundamental texts of Gaudiya Vaishnavism including Bhagavad-gita and essential scriptures."]="Estudio completo de los textos fundamentales del Gaudiya Vaishnavismo incluyendo el Bhagavad-gita y las escrituras esenciales."
    
    # Related book/course translations that might need fixing
    ["Back to Course"]="Regresar al Curso"
    ["Read Online (English)"]="Leer en Línea (Inglés)"
    ["Read Online (Spanish)"]="Leer en Línea (Español)"
    ["Read in English"]="Leer en Inglés"
    ["Read in Spanish"]="Leer en Español"
    ["Study Tools"]="Herramientas de Estudio"
    ["Study Questions"]="Preguntas de Estudio"
    ["Test your knowledge"]="Evaluar tu conocimiento"
    ["Take Quiz"]="Realizar Examen"
    ["Questions & Answers"]="Preguntas y Respuestas"
    ["Study Materials"]="Materiales de Estudio"
    ["Available Courses"]="Cursos Disponibles"
    ["Explore Course"]="Explorar Curso"
)

for english in "${!fixes[@]}"; do
    spanish="${fixes[$english]}"
    echo "📝 $english -> $spanish"
    
    # Escape special characters for sed
    escaped_english=$(printf '%s\n' "$english" | sed 's/[[\.*^$/]/\\&/g')
    escaped_spanish=$(printf '%s\n' "$spanish" | sed 's/[[\.*^$/]/\\&/g')
    
    # Update the translation
    sed -i "/msgid \"$escaped_english\"/{n;s/msgstr \".*\"/msgstr \"$escaped_spanish\"/}" "$PO_FILE"
done

echo ""
echo "✅ All requested translations updated!"
echo ""
echo "🔍 Verifying key changes:"
key_phrases=(
    "Back to Courses"
    "Study This Book" 
    "Read Online"
    "Comprehensive study of the fundamental texts"
)

for phrase in "${key_phrases[@]}"; do
    echo ""
    echo "$phrase:"
    grep -A 1 "msgid \"$phrase\"" "$PO_FILE" 2>/dev/null || echo "   (Not found or pattern different)"
done

echo ""
echo "🔨 Compiling messages..."
python3 manage.py compilemessages

echo ""
echo "🎉 All requested translations have been fixed!"
echo "🌐 Test at: http://localhost:8000/es/"
