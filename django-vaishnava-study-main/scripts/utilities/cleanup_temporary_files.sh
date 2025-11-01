#!/bin/bash
echo "🧹 CLEANING TEMPORARY FILES"
echo "==========================="

cd ~/django-vaishnava-study

# Remove temporary Python files
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Remove any remaining temporary shell scripts in root
find . -maxdepth 1 -name "*.sh" ! -name "manage.py" -exec mv {} scripts/backups/ \; 2>/dev/null || true

echo "✅ Temporary files cleaned up"
