#!/usr/bin/env python3
"""
Spanish Translation Helper for Vaishnava Study App
This script helps identify and manage Spanish translations.
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
django.setup()

from django.utils.translation import gettext as _

def check_common_vaishnava_terms():
    """Check common Vaishnava terms that need translation"""
    
    common_terms = [
        # App-specific terms
        "Vaishnava Study App",
        "Comprehensive study platform for ISKCON's Bhakti Shastri and advanced courses with multilingual support",
        "Available Courses",
        "Explore Course",
        "Take Quiz",
        "Quiz Results",
        "Study Materials",
        "Questions & Answers",
        "Upload Q&A",
        "Upload Study Materials",
        
        # Vaishnava terms
        "Bhakti Shastri",
        "Bhakti Vaibhava", 
        "Bhakti Vedanta",
        "Bhakti Sarvabhauma",
        "Bhagavad-gita",
        "Srimad Bhagavatam",
        "Chaitanya Charitamrita",
        "Nectar of Instruction",
        "Nectar of Devotion",
        
        # Common UI terms
        "Home",
        "Courses", 
        "Resources",
        "Contact",
        "Login",
        "Logout",
        "Admin",
        "Save",
        "Delete",
        "Edit",
        "Submit",
        "Cancel",
        
        # Quiz terms
        "Correct",
        "Incorrect",
        "Score",
        "Attempt",
        "Question",
        "Answer",
        "Explanation"
    ]
    
    print("=== COMMON TERMS TO TRANSLATE ===")
    for term in common_terms:
        print(f"English: {term}")
        print("Spanish: [Need translation]")
        print("---")

def find_untranslated_in_templates():
    """Find untranslated strings in templates"""
    
    template_dir = Path("study_app/templates")
    translatable_patterns = [
        "{% trans ",
        "{% blocktranslate %}",
        "_(",
        "gettext("
    ]
    
    print("=== CHECKING TEMPLATES FOR UNTRANSLATED STRINGS ===")
    
    for template_file in template_dir.rglob("*.html"):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for pattern in translatable_patterns:
            if pattern in content:
                print(f"File: {template_file}")
                print(f"Contains translatable strings with pattern: {pattern}")
                print("---")

if __name__ == "__main__":
    print("Vaishnava Study App - Spanish Translation Helper")
    print("=" * 50)
    
    check_common_vaishnava_terms()
    find_untranslated_in_templates()
    
    print("\nTo complete translations:")
    print("1. Edit the .po files in locale/es/LC_MESSAGES/")
    print("2. Add Spanish translations for each msgid")
    print("3. Run: python3 manage.py compilemessages")
    print("4. Restart your Django server")
