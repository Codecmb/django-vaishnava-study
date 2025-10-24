#!/bin/bash

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

backup_file() {
    local file="$1"
    local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$file" "$backup"
    log_info "Backed up: $backup"
}

# Move red language switcher into navbar and remove blue dropdown
move_red_switcher_to_navbar() {
    local file="./study_app/templates/study_app/includes/navbar.html"
    
    if [[ ! -f "$file" ]]; then
        log_error "Navbar file not found: $file"
        return 1
    fi
    
    log_info "Moving red language switcher into navbar and removing blue dropdown..."
    backup_file "$file"
    
    # Extract the red language switcher HTML
    local red_switcher=$(grep -A 5 "<!-- Red Language Switcher Button -->" "$file" | tail -n +2 | head -n 5)
    
    # Create new navbar with red switcher inside and blue dropdown removed
    awk '
    # Remove the blue dropdown language switcher (the form)
    /<form action="{% url .set_language. %}/ { skip_form = 1 }
    skip_form && /<\/form>/ { skip_form = 0; next }
    skip_form { next }
    
    # Remove the red switcher from its current position (we will add it back later)
    /<!-- Red Language Switcher Button -->/ { skip_red = 1 }
    skip_red && /<\/div>/ { skip_red = 0; next }
    skip_red { next }
    
    # Insert the red switcher right before the login section
    /{% if user.is_authenticated %}/ && !red_added {
        print "            <!-- Red Language Switcher Button -->"
        print "            <div style=\"display: inline-block; margin-left: 15px; background: #d32f2f; padding: 8px 12px; border-radius: 4px; border: 1px solid #ff6b6b;\">"
        print "                <a href=\"/en/\" style=\"color: white; margin: 0 8px; font-weight: bold; text-decoration: none; font-size: 14px;\">EN</a>"
        print "                <span style=\"color: white;\">|</span>"
        print "                <a href=\"/es/\" style=\"color: white; margin: 0 8px; font-weight: bold; text-decoration: none; font-size: 14px;\">ES</a>"
        print "            </div>"
        red_added = 1
    }
    
    { print }
    ' "$file" > "${file}.tmp"
    
    mv "${file}.tmp" "$file"
    log_info "✅ Red language switcher moved to navbar, blue dropdown removed"
}

# Also update vaishnava_study navbar
update_vaishnava_navbar() {
    local file="./study_app/templates/vaishnava_study/includes/navbar.html"
    
    if [[ ! -f "$file" ]]; then
        log_warn "Vaishnava navbar not found, skipping: $file"
        return 0
    fi
    
    log_info "Updating vaishnava navbar..."
    backup_file "$file"
    
    # Remove the blue dropdown and add red switcher
    awk '
    # Remove the blue dropdown language switcher (the form)
    /<form action="{% url .set_language. %}/ { skip_form = 1 }
    skip_form && /<\/form>/ { skip_form = 0; next }
    skip_form { next }
    
    # Insert red switcher before the closing div of nav-links
    /<\/div>[[:space:]]*<\/div>[[:space:]]*<\/nav>/ && !red_added {
        print "            <!-- Red Language Switcher Button -->"
        print "            <div style=\"display: inline-block; margin-left: 15px; background: #d32f2f; padding: 8px 12px; border-radius: 4px; border: 1px solid #ff6b6b;\">"
        print "                <a href=\"/en/\" style=\"color: white; margin: 0 8px; font-weight: bold; text-decoration: none; font-size: 14px;\">EN</a>"
        print "                <span style=\"color: white;\">|</span>"
        print "                <a href=\"/es/\" style=\"color: white; margin: 0 8px; font-weight: bold; text-decoration: none; font-size: 14px;\">ES</a>"
        print "            </div>"
        red_added = 1
    }
    
    { print }
    ' "$file" > "${file}.tmp"
    
    mv "${file}.tmp" "$file"
    log_info "✅ Vaishnava navbar updated"
}

main() {
    log_info "Moving red language switcher to navbar..."
    
    # Check if we're in the right directory
    if [[ ! -f "manage.py" ]]; then
        log_error "Please run this script from your Django project root directory"
        exit 1
    fi
    
    # Make modifications
    move_red_switcher_to_navbar
    update_vaishnava_navbar
    
    log_info "🎉 All modifications completed!"
    log_info "Summary:"
    log_info "  ✅ Blue dropdown language switcher removed"
    log_info "  ✅ Red EN/ES language button moved into navbar"
    log_info "  ✅ Both study_app and vaishnava_study navbars updated"
    log_info ""
    log_info "The navbar should now have:"
    log_info "  - Navigation links"
    log_info "  - Red 'Explorar Curso' button" 
    log_info "  - Red EN/ES language switcher"
    log_info "  - Login/Admin links"
}

main "$@"
