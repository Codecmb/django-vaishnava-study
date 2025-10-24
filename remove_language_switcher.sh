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

# First, let's find where the language switcher is
echo "=== SEARCHING FOR LANGUAGE SWITCHER ==="
find ./study_app/templates -name "*.html" -exec grep -l "language" {} \; | while read file; do
    echo "→ $file"
    grep -n -i "language" "$file" | head -10
done

echo ""
echo "=== SEARCHING FOR FORM WITH LANGUAGE SELECTION ==="
find ./study_app/templates -name "*.html" -exec grep -l "form" {} \; | while read file; do
    if grep -q -i "language" "$file"; then
        echo "→ $file"
        grep -n -A 5 -B 5 -i "language" "$file" | head -20
    fi
done

# Check navbar for existing red button
echo ""
echo "=== CURRENT NAVBAR CONTENT ==="
cat ./study_app/templates/study_app/includes/navbar.html
