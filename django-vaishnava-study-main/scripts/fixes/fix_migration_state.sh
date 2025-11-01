#!/bin/bash
echo "🔧 FIXING MIGRATION STATE"
echo "========================="

cd ~/django-vaishnava-study
source venv/bin/activate

# Check if migrations work now
echo "📋 Checking migration status..."
python manage.py showmigrations study_app

# Create a proper migration for the unique constraint
echo ""
echo "🔄 Creating proper migration..."
python manage.py makemigrations study_app --name add_unique_constraint

# Apply the migration
echo ""
echo "🔄 Applying migration..."
python manage.py migrate study_app

# Test the system
echo ""
echo "🧪 Testing system..."
python manage.py check
