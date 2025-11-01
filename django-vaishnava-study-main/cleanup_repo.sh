#!/bin/bash
echo "🧹 CLEANING REPOSITORY"
echo "======================"

echo "Removing temporary fix scripts..."
rm -f fix_*.py
rm -f *_conflict.py
rm -f *_stash.sh
rm -f *_helper.sh
rm -f *.md

echo "Keeping only project files:"
echo "✅ study_app/ - Django app with quiz system"
echo "✅ website/ - Project settings"
echo "✅ manage.py - Django management"
echo "✅ requirements.txt - Dependencies"
echo "✅ .gitignore - File exclusion rules"

echo ""
echo "Repository cleaned!"
