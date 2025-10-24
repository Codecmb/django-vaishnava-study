#!/bin/bash

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# Function to extract untranslated strings from PO files
find_untranslated_strings() {
    local po_file="$1"
    log_step "Checking untranslated strings in: $po_file"
    
    if [[ ! -f "$po_file" ]]; then
        log_error "PO file not found: $po_file"
        return 1
    fi
    
    # Count total messages and untranslated
    local stats=$(msgfmt --statistics "$po_file" 2>&1)
    echo "Translation status: $stats"
    
    # Extract untranslated messages (lines with msgid but empty msgstr)
    log_step "Untranslated strings:"
    awk '
    /^msgid "/ { 
        msgid = substr($0, 8, length($0)-8) 
        getline
        if (/^msgstr ""$/ || /^msgstr ".*[^"]"$/) {
            getline
            if (/^$/) {
                print msgid
            }
        }
    }
    ' "$po_file" | head -20
    
    echo ""
}

# Function to update PO files with new strings
update_po_files() {
    log_step "Updating PO files with new strings from templates and code..."
    
    # Extract strings from templates and Python files using python3
    python3 manage.py makemessages -l es -i "venv/*" --no-location
    
    log_info "✅ PO files updated with current strings"
}

# Function to compile translations
compile_translations() {
    log_step "Compiling translations..."
    python3 manage.py compilemessages
    log_info "✅ Translations compiled"
}

# Function to show translation progress
show_progress() {
    log_step "Current translation progress:"
    
    for po_file in $(find ./locale -name "*.po"); do
        echo "→ $(basename $(dirname $po_file))/$(basename $po_file)"
        msgfmt --statistics "$po_file" 2>&1 || echo "Error reading file"
        echo ""
    done
}

# Function to create a translation helper script
create_translation_helper() {
    local helper_file="translation_helper_es.py"
    
    log_step "Creating Spanish translation helper script..."
    
    cat > "$helper_file" << 'PYTHON_EOF'
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
PYTHON_EOF

    chmod +x "$helper_file"
    log_info "✅ Translation helper created: $helper_file"
}

main() {
    log_step "Starting Spanish translation process for Vaishnava Study App..."
    
    # Check if we're in the right directory
    if [[ ! -f "manage.py" ]]; then
        log_error "Please run this script from your Django project root directory"
        exit 1
    fi
    
    # Show current progress
    show_progress
    
    # Update PO files with current strings
    update_po_files
    
    # Check specific PO files for study_app
    local study_app_po="./locale/es/LC_MESSAGES/django.po"
    if [[ -f "$study_app_po" ]]; then
        find_untranslated_strings "$study_app_po"
    fi
    
    # Create translation helper
    create_translation_helper
    
    # Compile translations
    compile_translations
    
    log_info "🎉 Spanish translation setup completed!"
    log_info ""
    log_info "Next steps:"
    log_info "1. Run the translation helper: python3 translation_helper_es.py"
    log_info "2. Edit the PO files in: locale/es/LC_MESSAGES/"
    log_info "3. Add Spanish translations for each msgid"
    log_info "4. Test the Spanish version at: http://localhost:8000/es/"
    log_info ""
    log_info "Common PO file locations:"
    log_info "  - locale/es/LC_MESSAGES/django.po (for Python code)"
    log_info "  - locale/es/LC_MESSAGES/djangojs.po (for JavaScript)"
}

main "$@"
