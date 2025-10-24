#!/usr/bin/env python3
"""
Spanish Translation Assistant for Vaishnava Study App
Helps complete the remaining 74 translations efficiently.
"""

import os
import re
import subprocess
from pathlib import Path

class TranslationAssistant:
    def __init__(self):
        self.po_file = Path("./locale/es/LC_MESSAGES/django.po")
        self.project_root = Path(".")
        
    def get_translation_status(self):
        """Get current translation statistics"""
        if not self.po_file.exists():
            return "No PO file found"
        
        result = subprocess.run(
            ["msgfmt", "--statistics", str(self.po_file)], 
            capture_output=True, 
            text=True
        )
        return result.stderr.strip()
    
    def get_untranslated_strings(self, limit=20):
        """Get list of untranslated strings"""
        if not self.po_file.exists():
            return []
        
        with open(self.po_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find msgid with empty msgstr
        pattern = r'msgid "([^"]+)"\s*\nmsgstr ""'
        matches = re.findall(pattern, content)
        
        # Filter out empty and very short strings
        filtered = [m for m in matches if m and len(m) > 2 and m != '\\"']
        return filtered[:limit]
    
    def suggest_translations(self, english_text):
        """Suggest Spanish translations for common terms"""
        suggestions = {
            # Common UI elements
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
            
            # Study specific
            "Chapter": "Capítulo",
            "Verse": "Verso", 
            "Text": "Texto",
            "Note": "Nota",
            "Comment": "Comentario",
            "Reference": "Referencia",
            "Source": "Fuente",
            "Author": "Autor",
            
            # Status
            "Active": "Activo",
            "Inactive": "Inactivo", 
            "Pending": "Pendiente",
            "Approved": "Aprobado",
            "Rejected": "Rechazado",
            "Draft": "Borrador",
            "Published": "Publicado",
            
            # Common phrases
            "Please wait": "Por favor espere",
            "Thank you": "Gracias", 
            "Welcome": "Bienvenido",
            "Good luck": "Buena suerte",
            "Congratulations": "Felicidades",
            "Please try again": "Por favor intente nuevamente",
            "An error occurred": "Ocurrió un error",
        }
        
        return suggestions.get(english_text, "")
    
    def compile_translations(self):
        """Compile the translations"""
        result = subprocess.run(
            ["python3", "manage.py", "compilemessages"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def test_spanish_site(self):
        """Test if Spanish site is accessible"""
        try:
            # Start server briefly to test
            proc = subprocess.Popen(
                ["python3", "manage.py", "runserver", "0.0.0.0:8000"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            import time
            time.sleep(3)
            
            # Test the Spanish page
            import urllib.request
            response = urllib.request.urlopen("http://localhost:8000/es/")
            content = response.read().decode('utf-8')
            
            proc.terminate()
            proc.wait()
            
            return "Inicio" in content or "Cursos" in content
            
        except Exception as e:
            return False
    
    def show_work_progress(self):
        """Show progress and next steps"""
        status = self.get_translation_status()
        untranslated = self.get_untranslated_strings(15)
        
        print("=" * 60)
        print("🇪🇸 SPANISH TRANSLATION ASSISTANT")
        print("=" * 60)
        print()
        print(f"📊 Current Status: {status}")
        print()
        
        if untranslated:
            print("📝 NEXT 15 STRINGS TO TRANSLATE:")
            print("-" * 40)
            for i, text in enumerate(untranslated, 1):
                suggestion = self.suggest_translations(text)
                print(f"{i:2d}. {text}")
                if suggestion:
                    print(f"    💡 Sugerencia: {suggestion}")
                print()
        
        print("🔧 QUICK ACTIONS:")
        print("   1. Edit PO file: nano locale/es/LC_MESSAGES/django.po")
        print("   2. Find: msgstr \"\" and add Spanish text")
        print("   3. Compile: python3 manage.py compilemessages") 
        print("   4. Test: http://localhost:8000/es/")
        print()
        print("💡 TIP: Work in batches of 10-15 translations at a time!")

def main():
    assistant = TranslationAssistant()
    assistant.show_work_progress()
    
    # Test if basic setup works
    print("🧪 Testing basic setup...")
    if assistant.test_spanish_site():
        print("✅ Spanish site is accessible")
    else:
        print("⚠️  Could not test Spanish site (server may not be running)")
    
    print()
    print("🎯 You're ready to complete the Spanish translations!")
    print("   The system is fully configured and waiting for your Spanish text.")

if __name__ == "__main__":
    main()
