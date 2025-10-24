#!/bin/bash

# Script to modify Django templates - remove blue button and move red button to navbar

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Backup a file
backup_file() {
    local file="$1"
    local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$file" "$backup"
    log_info "Backed up: $backup"
}

# Modify the navbar to add the red button
modify_navbar() {
    local file="./study_app/templates/study_app/includes/navbar.html"
    
    if [[ ! -f "$file" ]]; then
        log_error "Navbar file not found: $file"
        return 1
    fi
    
    log_info "Modifying navbar: $file"
    backup_file "$file"
    
    # Create temporary file
    local temp_file="${file}.tmp"
    
    # Add the red button to navbar right before the closing div of nav-links
    awk '
    /<div style="display: flex; align-items: center; gap: 10px;">/ {
        print $0
        found_nav_links=1
        next
    }
    found_nav_links && /<\/div>/ && !button_added {
        print "            <button class=\"explore-btn\" style=\"background: #e74c3c; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 4px; cursor: pointer; font-weight: bold; margin-left: 1rem;\">Explorar Curso</button>"
        button_added=1
    }
    { print }
    ' "$file" > "$temp_file"
    
    mv "$temp_file" "$file"
    log_info "✅ Red button added to navbar"
}

# Remove blue button from index.html
modify_index() {
    local file="./study_app/templates/study_app/index.html"
    
    if [[ ! -f "$file" ]]; then
        log_error "Index file not found: $file"
        return 1
    fi
    
    log_info "Modifying index: $file"
    backup_file "$file"
    
    # Create temporary file
    local temp_file="${file}.tmp"
    
    # Remove any blue button from the courses section
    # Look for button patterns and remove them
    sed -E '/<button[^>]*style="[^"]*background:.*blue[^"]*"[^>]*>.*<\/button>/d' "$file" > "$temp_file"
    sed -E '/<button[^>]*style="[^"]*background.*#.*[0-9a-fA-F]*[^"]*"[^>]*>.*Explorar Curso.*<\/button>/d' "$temp_file" > "${temp_file}2"
    
    mv "${temp_file}2" "$file"
    rm -f "$temp_file"
    log_info "✅ Blue button removed from index page"
}

# Add CSS for the navbar button
add_navbar_css() {
    local css_file="./static/css/style.css"
    local main_css_file="./study_app/static/study_app/css/main.css"
    
    # Try to find the main CSS file
    if [[ -f "$main_css_file" ]]; then
        css_file="$main_css_file"
    elif [[ -f "$css_file" ]]; then
        css_file="$css_file"
    else
        log_warn "CSS file not found. Adding inline styles instead."
        return
    fi
    
    log_info "Adding navbar button styles to: $css_file"
    backup_file "$css_file"
    
    # Add navbar button styles if they don't exist
    if ! grep -q "explore-btn" "$css_file"; then
        cat >> "$css_file" << 'CSS_EOF'

/* Navbar Explore Button Styles */
.explore-btn {
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    color: white;
    border: none;
    padding: 0.7rem 1.5rem;
    border-radius: 25px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
    margin-left: 1rem;
}

.explore-btn:hover {
    background: linear-gradient(135deg, #c0392b, #a93226);
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(231, 76, 60, 0.4);
}

.explore-btn:active {
    transform: translateY(0);
}

/* Mobile responsive */
@media (max-width: 768px) {
    .explore-btn {
        margin-left: 0;
        margin-top: 0.5rem;
        width: 100%;
    }
}
CSS_EOF
        log_info "✅ Navbar button CSS added"
    else
        log_info "✅ Navbar button CSS already exists"
    fi
}

main() {
    log_info "Starting Django template modifications..."
    
    # Check if we're in the right directory
    if [[ ! -f "manage.py" ]]; then
        log_error "Please run this script from your Django project root directory"
        exit 1
    fi
    
    # Make modifications
    modify_navbar
    modify_index
    add_navbar_css
    
    log_info "🎉 All modifications completed!"
    log_info "Summary:"
    log_info "  ✅ Red 'Explorar Curso' button moved to navbar"
    log_info "  ✅ Blue button removed from course section"
    log_info "  ✅ Navbar button CSS styles added"
    log_info ""
    log_info "Next steps:"
    log_info "  1. Run your Django server: python manage.py runserver"
    log_info "  2. Check the homepage to see the changes"
    log_info "  3. If styles don't load, you may need to collect static files:"
    log_info "     python manage.py collectstatic"
}

main "$@"
