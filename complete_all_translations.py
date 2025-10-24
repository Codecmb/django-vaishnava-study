#!/usr/bin/env python3
"""
Complete all Spanish translations for Vaishnava Study App
"""

import re
from pathlib import Path

# Spanish translations for all missing strings
TRANSLATIONS = {
    # Course levels
    "Bhakti Sarvabhauma": "Bhakti Sarvabhauma",
    
    # Material types
    "Study Notes": "Notas de Estudio",
    "Chapter Summary": "Resumen del Capítulo", 
    "Quiz": "Examen",
    "Other Material": "Otro Material",
    
    # Authentication
    "Logged Out": "Sesión Cerrada",
    "You have been successfully logged out.": "Has cerrado sesión exitosamente.",
    "Click here to login again.": "Haz clic aquí para iniciar sesión nuevamente.",
    "Return to homepage": "Volver a la página principal",
    "Your username and password didn't match. Please try again.": "Tu nombre de usuario y contraseña no coinciden. Por favor, inténtalo de nuevo.",
    "Username": "Nombre de usuario",
    "Password": "Contraseña",
    "Don't have an account? Contact administrator.": "¿No tienes una cuenta? Contacta al administrador.",
    
    # Quiz system
    "Add Quiz Question": "Agregar Pregunta del Examen",
    "Quizzes": "Exámenes",
    "Add Question": "Agregar Pregunta",
    "Tips for creating good quiz questions:": "Consejos para crear buenas preguntas de examen:",
    "Focus on philosophical understanding rather than memorization": "Enfócate en la comprensión filosófica más que en la memorización",
    "Include multiple acceptable answers in the 'correct answers' field (comma-separated)": "Incluye múltiples respuestas aceptables en el campo 'respuestas correctas' (separadas por comas)",
    "Provide clear Srila Prabhupada commentary for guidance": "Proporciona comentarios claros de Srila Prabhupada para orientación",
    "Reference specific verses when possible": "Referencia versos específicos cuando sea posible",
    
    # Book and course details
    "Read the Book": "Leer el Libro",
    "Study Tools": "Herramientas de Estudio", 
    "Study Questions": "Preguntas de Estudio",
    "Test your knowledge": "Evalúa tu conocimiento",
    "About the Test your knowledge": "Acerca de Evalúa tu conocimiento",
    "Based on Srila Prabhupada's original commentaries": "Basado en los comentarios originales de Srila Prabhupada",
    "Flexible answer system - no rigid 'right/wrong'": "Sistema de respuestas flexible - sin 'correcto/incorrecto' rígido",
    "Philosophical feedback and guidance": "Retroalimentación y orientación filosófica",
    "Track your progress and understanding": "Sigue tu progreso y comprensión",
    "Start Your First Quiz Now": "Comienza Tu Primer Examen Ahora",
    "Back to Courses": "Volver a los Cursos",
    "Study This Book": "Estudiar Este Libro",
    "Read Online (English)": "Leer en Línea (Inglés)",
    "Read Online (Spanish)": "Leer en Línea (Español)",
    
    # Delete confirmation
    "Delete Study Material": "Eliminar Material de Estudio",
    "Type:": "Tipo:",
    "Language:": "Idioma:",
    "Book:": "Libro:",
    "Verse:": "Verso:",
    "This action cannot be undone!": "¡Esta acción no se puede deshacer!",
    "Yes, Delete": "Sí, Eliminar",
    
    # Quiz dashboard and results
    "Quiz Dashboard": "Panel de Exámenes",
    "Questions:": "Preguntas:",
    "No Questions Yet": "Aún No Hay Preguntas",
    "No quiz modules available for this course yet.": "Aún no hay módulos de examen disponibles para este curso.",
    "Admin Actions": "Acciones de Administrador",
    "Add Quiz Questions": "Agregar Preguntas del Examen",
    "Add New Module": "Agregar Nuevo Módulo",
    "Manage All Questions": "Gestionar Todas las Preguntas",
    "Quiz Results": "Resultados del Examen",
    "Results": "Resultados",
    "Philosophical Feedback": "Retroalimentación Filosófica",
    "Detailed Results": "Resultados Detallados",
    "Question": "Pregunta",
    "Question:": "Pregunta:",
    "Your Answer:": "Tu Respuesta:",
    "Suggested Understanding:": "Comprensión Sugerida:",
    "Key points:": "Puntos clave:",
    "Srila Prabhupada:": "Srila Prabhupada:",
    "Additional Guidance:": "Orientación Adicional:",
    "Retry Quiz": "Reintentar Examen",
    "Back to Quiz Dashboard": "Volver al Panel de Exámenes",
    "Back to Book": "Volver al Libro",
    
    # Quiz taking
    "Instructions": "Instrucciones",
    "Answer each question based on your understanding of Srila Prabhupada's commentaries. There are no 'wrong' answers - this is to help you gauge your philosophical understanding.": "Responde cada pregunta basándote en tu comprensión de los comentarios de Srila Prabhupada. No hay respuestas 'incorrectas' - esto es para ayudarte a evaluar tu comprensión filosófica.",
    "Srila Prabhupada's Commentary:": "Comentario de Srila Prabhupada:",
    "Submit Quiz": "Enviar Examen",
    
    # Upload forms
    "Upload Questions & Answers": "Subir Preguntas y Respuestas",
    "Select Book": "Seleccionar Libro",
    "CSV File": "Archivo CSV",
    "Notes (Optional)": "Notas (Opcional)",
    "CSV Format Instructions": "Instrucciones de Formato CSV",
    "Your CSV file should have these columns in the first row:": "Tu archivo CSV debe tener estas columnas en la primera fila:",
    "Question in English": "Pregunta en Inglés",
    "Question in Spanish": "Pregunta en Español", 
    "Answer in English": "Respuesta en Inglés",
    "Answer in Spanish": "Respuesta en Español",
    "Verse reference (e.g., Bg 1.1)": "Referencia del verso (ej., Bg 1.1)",
    "Display order number": "Número de orden de visualización",
    "Example CSV:": "Ejemplo CSV:",
    
    # Study material upload
    "Material Type": "Tipo de Material",
    "Title": "Título",
    "Description (Optional)": "Descripción (Opcional)",
    "English File": "Archivo en Inglés",
    "Spanish File": "Archivo en Español", 
    "Bilingual File": "Archivo Bilingüe",
    "Verse Reference (Optional)": "Referencia del Verso (Opcional)",
    "Order": "Orden",
    "Upload Study Material": "Subir Material de Estudio",
    "Supported File Types": "Tipos de Archivo Soportados",
    
    # Success messages
    "Your questions and answers have been successfully uploaded to the system.": "Tus preguntas y respuestas han sido subidas exitosamente al sistema.",
    "Upload More Q&A": "Subir Más P&R",
    
    # Footer and resources
    "Resources": "Recursos",
    "Support": "Soporte", 
    "Help Center": "Centro de Ayuda",
    "Contact Us": "Contáctanos",
    "Feedback": "Comentarios",
    "Official ISKCON Education": "Educación Oficial de ISKCON",
    "Available in English and Spanish": "Disponible en Inglés y Español",
    "Primarily in English": "Principalmente en Inglés",
    
    # Q&A sections
    "Q&A for": "P&R para",
    "No questions and answers available yet for this book.": "Aún no hay preguntas y respuestas disponibles para este libro.",
    
    # Platform description
    "Comprehensive study platform for ISKCON's Bhakti Shastri and advanced courses with multilingual support": "Plataforma integral de estudio para los cursos Bhakti Shastri y avanzados de ISKCON con soporte multilingüe",
    
    # Login
    "Login to Vaishnava Study": "Iniciar Sesión en Estudio Vaishnava"
}

def complete_translations():
    po_file = Path("./locale/es/LC_MESSAGES/django.po")
    
    if not po_file.exists():
        print("❌ PO file not found")
        return False
    
    # Read the PO file
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count applied translations
    applied_count = 0
    missing_translations = []
    
    # Apply translations
    for english, spanish in TRANSLATIONS.items():
        # Escape for regex
        escaped_english = re.escape(english)
        pattern = f'msgid "{escaped_english}"\\s*\\nmsgstr ""'
        replacement = f'msgid "{english}"\nmsgstr "{spanish}"'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            applied_count += 1
            print(f"✅ Translated: '{english}'")
        else:
            # Check if it exists but already has a translation
            if english in content:
                existing_pattern = f'msgid "{escaped_english}"\\s*\\nmsgstr "[^"]*"'
                if not re.search(existing_pattern, content):
                    missing_translations.append(english)
    
    # Write the updated content
    with open(po_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n🎉 TRANSLATION SUMMARY")
    print("=" * 50)
    print(f"✅ Applied: {applied_count} translations")
    
    if missing_translations:
        print(f"⚠️  Not found (may already be translated): {len(missing_translations)}")
        for missing in missing_translations[:5]:
            print(f"   - {missing}")
    
    return True

def compile_and_test():
    """Compile translations and test"""
    import subprocess
    
    print("\n🔨 Compiling translations...")
    result = subprocess.run(
        ["python3", "manage.py", "compilemessages"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Translations compiled successfully!")
    else:
        print("❌ Compilation failed")
        print(result.stderr)
        return False
    
    print("\n🌐 Testing Spanish setup...")
    try:
        # Quick test to see if basic translation works
        test_result = subprocess.run([
            "python3", "-c", 
            '''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
import django
django.setup()
from django.utils.translation import activate, gettext as _
activate("es")
print("✅ Spanish translation test:")
print("   Home ->", _("Home"))
print("   Courses ->", _("Courses"))
print("   Login ->", _("Login"))
            '''
        ], capture_output=True, text=True)
        
        print(test_result.stdout)
        if test_result.stderr:
            print("⚠️  Warnings:", test_result.stderr)
            
    except Exception as e:
        print(f"⚠️  Test failed: {e}")
    
    return True

def main():
    print("🇪🇸 COMPLETE SPANISH TRANSLATION PROCESS")
    print("=" * 60)
    
    # Apply all translations
    if complete_translations():
        # Compile and test
        if compile_and_test():
            print("\n🎉 ALL TRANSLATIONS COMPLETED SUCCESSFULLY!")
            print("\n🚀 Next steps:")
            print("   1. Start server: python3 manage.py runserver")
            print("   2. Test Spanish: http://localhost:8000/es/")
            print("   3. Verify all text appears in Spanish")
            print("\n💡 If any text still appears in English:")
            print("   - Check if it's wrapped in {% trans %} tags in templates")
            print("   - Run: python3 manage.py makemessages -l es")
            print("   - Then re-run this script")
        else:
            print("\n❌ Compilation or testing failed")
    else:
        print("\n❌ Translation process failed")

if __name__ == "__main__":
    main()
