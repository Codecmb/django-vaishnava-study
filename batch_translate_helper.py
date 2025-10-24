#!/usr/bin/env python3
"""
Batch translation helper for remaining 74 strings
"""

import os
import re

# Common translations for the remaining strings
COMMON_TRANSLATIONS = {
    # Navigation and UI
    "All Courses": "Todos los Cursos",
    "Upload": "Subir",
    "Resources": "Recursos",
    "Contact": "Contacto",
    "Settings": "Configuración",
    "Profile": "Perfil",
    "Dashboard": "Panel de Control",
    "Search": "Buscar",
    "Filter": "Filtrar",
    "Sort": "Ordenar",
    
    # Actions
    "Add": "Agregar",
    "Create": "Crear",
    "Update": "Actualizar",
    "Remove": "Remover",
    "Continue": "Continuar",
    "Finish": "Finalizar",
    "Start": "Comenzar",
    "End": "Terminar",
    
    # Status messages
    "Success": "Éxito",
    "Error": "Error",
    "Warning": "Advertencia",
    "Info": "Información",
    "Loading": "Cargando",
    "Processing": "Procesando",
    "Completed": "Completado",
    "Failed": "Fallido",
    
    # Forms and inputs
    "Username": "Nombre de Usuario",
    "Password": "Contraseña",
    "Email": "Correo Electrónico",
    "Name": "Nombre",
    "Description": "Descripción",
    "Title": "Título",
    "Content": "Contenido",
    "File": "Archivo",
    "Image": "Imagen",
    "Document": "Documento",
    
    # Quiz and study terms
    "Quiz": "Examen",
    "Test": "Prueba",
    "Exam": "Evaluación",
    "Practice": "Práctica",
    "Review": "Revisar",
    "Study": "Estudiar",
    "Learn": "Aprender",
    "Chapter": "Capítulo",
    "Verse": "Verso",
    "Text": "Texto",
    
    # Spiritual terms (keep some in English if they're proper names)
    "Spiritual": "Espiritual",
    "Divine": "Divino",
    "Sacred": "Sagrado",
    "Scripture": "Escritura",
    "Teaching": "Enseñanza",
    "Wisdom": "Sabiduría",
    "Knowledge": "Conocimiento",
    "Devotion": "Devoción",
    "Service": "Servicio",
    
    # Common phrases
    "Please wait": "Por favor espere",
    "Thank you": "Gracias",
    "Welcome": "Bienvenido",
    "Good luck": "Buena suerte",
    "Congratulations": "Felicidades",
}

def suggest_translation(english_text):
    """Suggest Spanish translation for common patterns"""
    
    # If it's already in our dictionary, use that
    if english_text in COMMON_TRANSLATIONS:
        return COMMON_TRANSLATIONS[english_text]
    
    # Common patterns
    patterns = {
        r"^Add (.+)$": lambda m: f"Agregar {m.group(1)}",
        r"^Create (.+)$": lambda m: f"Crear {m.group(1)}", 
        r"^Edit (.+)$": lambda m: f"Editar {m.group(1)}",
        r"^Delete (.+)$": lambda m: f"Eliminar {m.group(1)}",
        r"^Update (.+)$": lambda m: f"Actualizar {m.group(1)}",
        r"^View (.+)$": lambda m: f"Ver {m.group(1)}",
        r"^Manage (.+)$": lambda m: f"Gestionar {m.group(1)}",
        r"^Select (.+)$": lambda m: f"Seleccionar {m.group(1)}",
        r"^Choose (.+)$": lambda m: f"Elegir {m.group(1)}",
        r"^Search (.+)$": lambda m: f"Buscar {m.group(1)}",
    }
    
    for pattern, translator in patterns.items():
        match = re.match(pattern, english_text)
        if match:
            return translator(match)
    
    # Default: return empty for manual translation
    return ""

def main():
    po_file = "./locale/es/LC_MESSAGES/django.po"
    
    if not os.path.exists(po_file):
        print("❌ PO file not found")
        return
    
    print("=== BATCH TRANSLATION HELPER ===")
    print(f"📁 Working with: {po_file}")
    print()
    
    # Read the PO file
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all untranslated strings
    untranslated = re.findall(r'msgid "([^"]+)"\s*\nmsgstr ""', content)
    
    print(f"📊 Found {len(untranslated)} untranslated strings")
    print()
    
    # Show suggestions for first 20
    print("🔍 Translation suggestions (first 20):")
    print("=" * 50)
    
    for i, english in enumerate(untranslated[:20]):
        if english and english != '\\"':
            suggestion = suggest_translation(english)
            print(f"{i+1}. ENGLISH: {english}")
            if suggestion:
                print(f"   SUGGESTION: {suggestion}")
            else:
                print(f"   SUGGESTION: [Manual translation needed]")
            print()
    
    print("💡 To add these translations:")
    print("   1. Edit the PO file directly")
    print("   2. Find each 'msgstr \"\"' line") 
    print("   3. Replace with 'msgstr \"Spanish text\"'")
    print("   4. Run: python3 manage.py compilemessages")
    print()
    print("🌐 Test at: http://localhost:8000/es/")

if __name__ == "__main__":
    main()
