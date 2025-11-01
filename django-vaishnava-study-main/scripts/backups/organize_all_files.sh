#!/bin/bash
echo "🗂️ ORGANIZING ALL PROJECT FILES"
echo "=============================="

cd ~/django-vaishnava-study

# Create organized directory structure
mkdir -p scripts/{fixes,tests,backups,utilities} logs backups

echo "📁 Created directory structure"

# Move all script files to appropriate directories
echo "📦 Moving script files..."

# Fix scripts
mv fix_*.sh scripts/fixes/ 2>/dev/null || echo "No fix scripts to move"
mv add_*.sh scripts/fixes/ 2>/dev/null || echo "No add scripts to move"
mv clean_*.sh scripts/fixes/ 2>/dev/null || echo "No clean scripts to move"
mv force_*.sh scripts/fixes/ 2>/dev/null || echo "No force scripts to move"
mv enable_*.sh scripts/fixes/ 2>/dev/null || echo "No enable scripts to move"
mv apply_*.sh scripts/fixes/ 2>/dev/null || echo "No apply scripts to move"

# Test scripts
mv test_*.sh scripts/tests/ 2>/dev/null || echo "No test scripts to move"
mv test_*.py scripts/tests/ 2>/dev/null || echo "No test Python scripts to move"
mv verify_*.sh scripts/tests/ 2>/dev/null || echo "No verify scripts to move"
mv check_*.sh scripts/tests/ 2>/dev/null || echo "No check scripts to move"
mv debug_*.sh scripts/tests/ 2>/dev/null || echo "No debug scripts to move"
mv examine_*.sh scripts/tests/ 2>/dev/null || echo "No examine scripts to move"

# Utility scripts
mv restart_*.sh scripts/utilities/ 2>/dev/null || echo "No restart scripts to move"
mv hard_*.sh scripts/utilities/ 2>/dev/null || echo "No hard refresh scripts to move"
mv use_*.sh scripts/utilities/ 2>/dev/null || echo "No use scripts to move"
mv final_*.sh scripts/utilities/ 2>/dev/null || echo "No final scripts to move"
mv create_*.sh scripts/utilities/ 2>/dev/null || echo "No create scripts to move"
mv discover_*.sh scripts/utilities/ 2>/dev/null || echo "No discover scripts to move"

# Backup files
mv *.backup* scripts/backups/ 2>/dev/null || echo "No backup files to move"
mv *backup* scripts/backups/ 2>/dev/null || echo "No backup files to move"

# CSV templates
mv *.csv scripts/utilities/ 2>/dev/null || echo "No CSV files to move"

# Make all scripts executable
chmod +x scripts/fixes/*.sh 2>/dev/null || true
chmod +x scripts/tests/*.sh 2>/dev/null || true
chmod +x scripts/utilities/*.sh 2>/dev/null || true

echo "✅ All scripts organized and made executable"

# Create a cleanup script to remove temporary files
cat > scripts/utilities/cleanup_temporary_files.sh << 'CLEANUP_EOF'
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
CLEANUP_EOF

chmod +x scripts/utilities/cleanup_temporary_files.sh

# Run cleanup
./scripts/utilities/cleanup_temporary_files.sh

echo ""
echo "📋 FINAL PROJECT STRUCTURE:"
ls -la

echo ""
echo "📁 ORGANIZED SCRIPTS:"
find scripts -type f -name "*.sh" -o -name "*.py" | sort
