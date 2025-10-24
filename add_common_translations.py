#!/usr/bin/env python3
"""
Script to add common Spanish translations to the PO file
"""

import os
import re

# Common translations dictionary
TRANSLATIONS = {
    "Vaishnava Study App": "Aplicación de Estudio Vaishnava",
    "Comprehensive study platform for ISKCON's Bhakti Shastri and advanced courses with multilingual support": 
        "Plataforma integral de estudio para los cursos Bhakti Shastri y avanzados de ISKCON con soporte multilingüe",
    "Available Courses": "Cursos Disponibles",
    "Explore Course": "Explorar Curso",
    "Take Quiz": "Realizar Examen",
    "Study Materials": "Materiales de Estudio",
    "Questions & Answers": "Preguntas y Respuestas",
    "Upload Q&A": "Subir P&R",
    "Upload Study Materials": "Subir Materiales de Estudio",
    "Home": "Inicio",
    "Courses": "Cursos",
    "Login": "Iniciar Sesión",
    "Logout": "Cerrar Sesión",
    "Admin": "Administración",
    "Save": "Guardar",
    "Delete": "Eliminar",
    "Edit": "Editar",
    "Submit": "Enviar",
    "Cancel": "Cancelar",
    "Bhakti Shastri": "Bhakti Shastri",
    "Bhakti Vaibhava": "Bhakti Vaibhava",
    "Bhakti Vedanta": "Bhakti Vedanta",
    "Bhagavad-gita": "Bhagavad-gita",
    "Srimad Bhagavatam": "Srimad Bhagavatam",
    "Correct": "Correcto",
    "Incorrect": "Incorrecto",
    "Score": "Puntuación",
    "Question": "Pregunta",
    "Answer": "Respuesta",
    "Back to Courses": "Volver a Cursos",
    "Back to Course": "Volver al Curso",
    "Choose Your Study Method": "Elige Tu Método de Estudio",
    "Reference Websites": "Sitios Web de Referencia",
    "No courses available yet.": "Aún no hay cursos disponibles.",
    "Please check back later or contact the administrator.": "Por favor, vuelva más tarde o contacte al administrador.",
    "Upload Successful!": "¡Subida Exitosa!",
    "Your questions and answers have been successfully uploaded to the system.": 
        "Tus preguntas y respuestas han sido subidas exitosamente al sistema.",
    "Upload More Q&A": "Subir Más P&R",
    "Return to Dashboard": "Volver al Panel",
    "Are you sure you want to delete?": "¿Estás seguro de que quieres eliminar?",
    "Delete Study Material": "Eliminar Material de Estudio",
}

def add_translations(po_file_path):
    """Add translations to the PO file"""
    
    if not os.path.exists(po_file_path):
        print(f"❌ PO file not found: {po_file_path}")
        return
    
    # Read the entire file
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count how many translations we're adding
    added_count = 0
    
    # Replace empty msgstr with translations
    for english, spanish in TRANSLATIONS.items():
        # Escape special characters for regex
        escaped_english = re.escape(english)
        pattern = f'msgid "{escaped_english}"\\s*\\nmsgstr ""'
        replacement = f'msgid "{english}"\nmsgstr "{spanish}"'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            added_count += 1
            print(f"✅ Added: '{english}' -> '{spanish}'")
    
    # Write the updated content back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n🎉 Added {added_count} Spanish translations")
    print(f"Updated file: {po_file_path}")

if __name__ == "__main__":
    po_file = "./locale/es/LC_MESSAGES/django.po"
    add_translations(po_file)
    
    print("\n🔨 Now compiling translations...")
    os.system("python3 manage.py compilemessages")
    
    print("\n🌐 You can now test Spanish at: http://localhost:8000/es/")
